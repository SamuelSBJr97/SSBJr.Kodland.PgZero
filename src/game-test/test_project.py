from game.project import Depurador
from game.game import Game


def test_project_builds_and_attaches():
    proj = Depurador("TestCity")
    g = Game()
    proj.attach_to_game(g)
    assert g.running
