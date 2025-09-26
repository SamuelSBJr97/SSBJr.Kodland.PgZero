"""Pacote base do jogo.

Contém classes base leves para construir jogos com Pygame Zero (pgzero).
Estas classes evitam dependências diretas de pgzero para facilitar testes.
"""

from .base import GameObject, BaseGame
from .scene import Scene, SceneManager
from .game import Game
from .entities import (
	Jogador,
	Sala,
	Guardiao,
	Livro,
	Mapa,
	Cidade,
	Estrada,
	UILivro,
	UIQuestionario,
	UIHud,
)
from .project import SalasEQuestoes

__all__ = [
	"GameObject",
	"BaseGame",
	"Scene",
	"SceneManager",
	"Game",
	"Jogador",
	"Sala",
	"Guardiao",
	"Livro",
	"Mapa",
	"Cidade",
	"Estrada",
	"UILivro",
	"UIQuestionario",
	"UIHud",
	"SalasEQuestoes",
]
