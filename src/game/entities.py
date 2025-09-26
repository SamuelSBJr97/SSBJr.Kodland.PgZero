"""Entidades do jogo: jogador, salas, guardiões, livros, mapa, UI simples.

Estas implementações são leves — focadas em estrutura e testabilidade —
e não assumem objetos gráficos concretos (mantêm dados e hooks draw/update).
"""
from typing import List, Optional, Dict, Any
from .base import GameObject

class Bug(GameObject):
    def __init__(self, name: str, x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.name = name
        self.dialogue: List[str] = []
        # exemplo de estado para movimentação
        self.speed: float = 1.0  # unidades por segundo
        self._target: Optional[tuple] = None

    def attack(self) -> Optional[str]:
        return self.dialogue[0] if self.dialogue else None

    def compute_next_state(self, dt: float) -> Optional[Dict[str, Any]]:
        """Calcula próximo estado sem mutar atributos. Retorna dict com alterações.

        Implementação simples: se existir _target, move na direção linear em x/y
        até alcançá-lo, retornando a nova posição.
        """
        if not self._target:
            return None
        tx, ty = self._target
        dx = tx - self.x
        dy = ty - self.y
        dist = (dx * dx + dy * dy) ** 0.5
        if dist == 0:
            return None
        step = self.speed * dt
        if step >= dist:
            # alcançado
            return {'pos': (tx, ty)}
        nx = self.x + dx / dist * step
        ny = self.y + dy / dist * step
        return {'pos': (nx, ny)}

    def apply_state(self, state: Optional[Dict[str, Any]]) -> None:
        # usa implementação genérica para atualizar pos
        super().apply_state(state)

    def set_target(self, x: float, y: float) -> None:
        self._target = (float(x), float(y))

class Component(GameObject):
    def __init__(self, name: str, description: str = "", x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.name = name
        self.description = description
        self.items: List[GameObject] = []
        self.bugs: List[Bug] = []

    def add_item(self, item: GameObject) -> None:
        self.items.append(item)

    def add_bug(self, g: Bug) -> None:
        self.bugs.append(g)

class Cell(GameObject):
    def __init__(self, name: str, description: str = "", x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.name = name
        self.description = description
        self.items: List[GameObject] = []
        self.bugs: List[Bug] = []

    def add_item(self, item: GameObject) -> None:
        self.items.append(item)

    def add_bug(self, g: Bug) -> None:
        self.bugs.append(g)

class Player(GameObject):
    def __init__(self, name: str = "Debugger", x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.name = name
        self.health: int = 10
        self.move_queue: List[tuple] = []

    def compute_next_state(self, dt: float) -> Optional[Dict[str, Any]]:
        """Processa um movimento por célula enfileirado sem aplicar mutações.

        Retorna {'pos': (x, y)} se houver um movimento a aplicar.
        """
        if not self.move_queue:
            return None
        # simples: pega o próximo destino
        nx, ny = self.move_queue[0]
        return {'pos': (nx, ny)}

    def apply_state(self, state: Optional[Dict[str, Any]]) -> None:
        if not state:
            return
        pos = state.get('pos')
        if pos is not None:
            # se aplicamos um movimento, consumimos a fila
            try:
                x, y = pos
                self.set_pos(x, y)
                if self.move_queue:
                    self.move_queue.pop(0)
            except Exception:
                pass

    def attack(self) -> None:
        pass


class Map:
    """Representação simples de mapa com salas conectadas."""

    def __init__(self):
        self.rooms: Dict[str, Component] = {}
        self.connections: Dict[str, List[str]] = {}

    def add_room(self, room: Component) -> None:
        self.rooms[room.name] = room

    def connect(self, a: str, b: str) -> None:
        self.connections.setdefault(a, []).append(b)
        self.connections.setdefault(b, []).append(a)


class Board(Map):
    def __init__(self, name: str):
        super().__init__()
        self.name = name


class Path(Map):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

class UIHud:
    """HUD simples que mostra status do jogador."""

    def __init__(self, player: Player):
        self.player = player

    def render(self, surface: Any) -> None:
        # Apenas placeholder
        pass
