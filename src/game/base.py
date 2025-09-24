"""Classes base leves para objetos e jogo.

Estas classes são pensadas para serem fáceis de testar sem depender do loop
de pgzero. Elas expõem métodos hook que podem ser usados por um wrapper
de integração com pgzero se necessário.
"""
from typing import Tuple, Optional, List


class GameObject:
    """Objeto de jogo básico.

    Responsabilidades:
    - manter posição (x, y)
    - manter visibilidade e ativo/inativo
    - fornecer hooks update(dt) e draw(surface)
    """

    def __init__(self, x: float = 0.0, y: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.visible = True
        self.active = True

    @property
    def pos(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def set_pos(self, x: float, y: float) -> None:
        self.x = float(x)
        self.y = float(y)

    def update(self, dt: float) -> None:
        """Atualiza o estado do objeto. dt é o delta time em segundos."""
        pass

    def draw(self, surface) -> None:
        """Desenha o objeto na surface (modo pgzero/pygame)."""
        pass


class BaseGame:
    """Gerenciador simples de jogo.

    Mantém uma lista de GameObject, provê update/draw e utilitários.
    Projetado para ser usado tanto em testes quanto integrado ao pgzero.
    """

    def __init__(self):
        self.objects: List[GameObject] = []
        self.width: Optional[int] = None
        self.height: Optional[int] = None

    def add(self, obj: GameObject) -> None:
        self.objects.append(obj)

    def remove(self, obj: GameObject) -> None:
        if obj in self.objects:
            self.objects.remove(obj)

    def update(self, dt: float) -> None:
        """Chama update em todos objetos ativos."""
        for obj in list(self.objects):
            if obj.active:
                obj.update(dt)

    def draw(self, surface) -> None:
        """Chama draw em todos objetos visíveis."""
        for obj in self.objects:
            if obj.visible:
                obj.draw(surface)

    def clear(self) -> None:
        self.objects.clear()
