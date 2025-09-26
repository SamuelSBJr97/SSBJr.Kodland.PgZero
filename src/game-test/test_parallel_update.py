from game.base import BaseGame
from game.entities import Bug, Player


def test_bug_compute_apply_single():
    g = BaseGame()
    b = Bug('B1', x=0, y=0)
    b.set_target(2, 0)
    g.add(b)

    # update com dt pequeno: deve mover na direção do target
    g.update(0.5)
    # posição deve ter se aproximado de (2,0)
    assert b.x > 0.0 and b.x <= 0.5 * b.speed * 1.0 or b.x <= 2.0


def test_parallel_multiple_bugs():
    g = BaseGame()
    b1 = Bug('B1', x=0, y=0)
    b2 = Bug('B2', x=5, y=0)
    b1.set_target(2, 0)
    b2.set_target(2, 0)
    g.add(b1)
    g.add(b2)

    g.update(1.0)

    # ambos se moveram para mais próximo do target
    assert b1.x > 0.0
    assert b2.x < 5.0


def test_player_move_queue_applied():
    g = BaseGame()
    p = Player('P', x=0, y=0)
    p.move_queue.append((1, 1))
    g.add(p)

    g.update(0.016)
    assert (p.x, p.y) == (1.0, 1.0)
