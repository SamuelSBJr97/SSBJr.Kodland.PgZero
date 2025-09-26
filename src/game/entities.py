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

    def attack(self) -> Optional[str]:
        return self.dialogue[0] if self.dialogue else None

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
