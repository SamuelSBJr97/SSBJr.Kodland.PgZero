import pytest
from game.base import GameObject, BaseGame


class Dummy(GameObject):
    def __init__(self):
        super().__init__(0, 0)
        self.updated = False
        self.drawn = False

    def update(self, dt: float) -> None:
        self.updated = True

    def draw(self, surface) -> None:
        self.drawn = True


def test_gameobject_position():
    d = Dummy()
    assert d.pos == (0.0, 0.0)
    d.set_pos(10, 20)
    assert d.pos == (10.0, 20.0)


def test_basegame_update_draw():
    game = BaseGame()
    d = Dummy()
    game.add(d)
    game.update(0.016)
    assert d.updated
    game.draw(None)
    assert d.drawn


def test_remove_and_clear():
    game = BaseGame()
    d = Dummy()
    game.add(d)
    game.remove(d)
    assert d not in game.objects
    game.add(d)
    game.clear()
    assert len(game.objects) == 0
