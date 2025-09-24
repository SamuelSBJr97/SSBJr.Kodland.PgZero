"""Script de execução para jogos baseados nas classes deste pacote.

Tenta integrar com pgzero se estiver instalado. Se pgzero não estiver
disponível, fornece uma função `run_headless` que executa algumas iterações
do loop update/draw para facilitar testes / desenvolvimento sem dependências.
"""
from typing import Optional
import time

from .game import Game


def run_headless(game: Game, steps: int = 5, dt: float = 1.0 / 60.0) -> None:
    """Roda o jogo algumas iterações chamando update/draw com surface=None.

    Útil para testes sem pgzero.
    """
    game.start()
    for _ in range(steps):
        game.update(dt)
        game.draw(None)
        time.sleep(0)  # yield
    game.stop()


def run_with_pgz(game: Game) -> None:
    """Tenta integrar com pgzero (pgzrun). Espera que exista um objeto
    global `game_instance` que o pgzero/pgzrun irá utilizar.
    """
    try:
        import pgzrun
    except Exception as e:
        raise RuntimeError("pgzero/pgzrun não está disponível: %s" % e)

    # pgzero espera que existam funções update() e draw() no módulo global.
    # Vamos anexar functions que delegam para a instância de Game.

    # Criar variável global que o usuário pode sobrescrever se quiser.
    global game_instance  # type: Optional[Game]
    game_instance = game

    def _update(delta: float = 1.0 / 60.0):
        # pgzero chama update() sem argumentos; não há valor de dt fácil
        # então passamos uma constante aproximada.
        if game_instance:
            game_instance.update(delta)

    def _draw():
        if game_instance:
            game_instance.draw(None)  # pgzero espera um objeto screen global

    # Expor no módulo global para pgzrun
    globals()["update"] = _update
    globals()["draw"] = _draw

    # Iniciar e rodar com pgzrun
    game.start()
    pgzrun.go()


if __name__ == "__main__":
    # Exemplo mínimo quando executado diretamente; roda headless.
    g = Game()
    print("Executando headless de exemplo (5 passos)...")
    run_headless(g)
