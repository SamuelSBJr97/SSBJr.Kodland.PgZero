"""Controlador principal do jogo.

Contém a classe Game que encapsula um SceneManager e provê métodos
fáceis de integrar com a API do pgzero (update/draw).
"""
from typing import Optional
from .scene import SceneManager, Scene

class Game:
    """Classe que controla o jogo principal.

    Responsabilidades:
    - armazenar SceneManager
    - delegar update/draw para a cena atual
    - utilitários para trocar/push/pop de cenas
    """

    def __init__(self, width: int = 800, height: int = 600):
        self.width = width
        self.height = height
        self.scenes = SceneManager()
        self.running = False

    def start(self, initial_scene: Optional[Scene] = None) -> None:
        """Inicia o jogo com uma cena inicial opcional."""
        if initial_scene is not None:
            self.scenes.push(initial_scene)
        self.running = True

    def stop(self) -> None:
        self.running = False

    # Scene helper wrappers
    def push_scene(self, scene: Scene) -> None:
        self.scenes.push(scene)

    def pop_scene(self) -> Optional[Scene]:
        return self.scenes.pop()

    def replace_scene(self, scene: Scene) -> None:
        self.scenes.replace(scene)

    # Core loop hooks
    def update(self, dt: float) -> None:
        if not self.running:
            return
        self.scenes.update(dt)

    def draw(self, surface) -> None:
        if not self.running:
            return
        self.scenes.draw(surface)
