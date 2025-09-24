"""Gerenciamento de cenas/estados do jogo.

Scene representa um estado do jogo com sua própria lista de objetos.
SceneManager troca e gerencia pilha de cenas.
"""
from typing import List, Optional
from .base import GameObject, BaseGame


class Scene(BaseGame):
    """Uma cena é um jogo pequeno com ciclo próprio."""

    def __init__(self, name: str = ""):
        super().__init__()
        self.name = name

    def on_enter(self, prev_scene: Optional["Scene"]) -> None:
        """Chamado quando a cena é ativada."""
        pass

    def on_exit(self, next_scene: Optional["Scene"]) -> None:
        """Chamado quando a cena é desativada."""
        pass


class SceneManager:
    """Gerencia troca entre cenas, suporta pilha de cenas simples."""

    def __init__(self):
        self._stack: List[Scene] = []

    def push(self, scene: Scene) -> None:
        prev = self.current if self._stack else None
        self._stack.append(scene)
        scene.on_enter(prev)

    def pop(self) -> Optional[Scene]:
        if not self._stack:
            return None
        top = self._stack.pop()
        nxt = self.current if self._stack else None
        top.on_exit(nxt)
        return top

    @property
    def current(self) -> Optional[Scene]:
        return self._stack[-1] if self._stack else None

    def replace(self, scene: Scene) -> None:
        prev = self.pop()
        self.push(scene)

    def update(self, dt: float) -> None:
        current = self.current
        if current:
            current.update(dt)

    def draw(self, surface) -> None:
        current = self.current
        if current:
            current.draw(surface)
