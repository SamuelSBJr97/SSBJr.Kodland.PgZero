"""Definição do projeto do jogo 'Depurador'.

Esta classe monta um mapa de exemplo, cria o jogador e organiza salas,
livros e guardiões para formar uma cena inicial utilizável pelo `Game`.
"""
from typing import Optional
from .game import Game
from .entities import 

class Debugger:
    """Classe que configura o mundo do jogo e fornece helpers para iniciar.

    Exemplo mínimo:
    - cria uma cidade com duas salas conectadas
    - adiciona um jogador e um livro
    - expõe `attach_to_game(game: Game)` para empurrar a cena inicial
    """

    def __init__(self, city_name: str = "CidadeExemplo"):
        self.city = Cidade(city_name)
        self.player: Optional[Jogador] = None
        self._build_example()

    def _build_example(self) -> None:
        s1 = Sala("Biblioteca", "Uma sala cheia de livros")
        s2 = Sala("Praça", "Uma praça central")

        book = Livro(id="livro1", title="O Primeiro Livro")
        s1.add_item(book)

        g = Guardiao("Guardiao Velho")
        g.dialogue.append("Responda à pergunta para seguir adiante.")
        s2.add_guardian(g)

        self.city.add_room(s1)
        self.city.add_room(s2)
        self.city.connect("Biblioteca", "Praça")

        self.player = Jogador("Herói")

    def attach_to_game(self, game: Game) -> None:
        """Anexa o estado inicial ao Game. Atualmente apenas empurra
        uma cena simplificada contendo o jogador e as salas.
        """
        # Como ainda não implementamos cenas ricas, apenas inicializamos
        # o jogo e marcaremos running=True; consumidores podem usar
        # game.scenes.push(...) com cenas customizadas.
        game.start()
