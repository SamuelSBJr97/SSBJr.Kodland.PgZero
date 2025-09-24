"""Pacote base do jogo.

Contém classes base leves para construir jogos com Pygame Zero (pgzero).
Estas classes evitam dependências diretas de pgzero para facilitar testes.
"""

from .base import GameObject, BaseGame
from .scene import Scene, SceneManager

__all__ = ["GameObject", "BaseGame", "Scene", "SceneManager"]
