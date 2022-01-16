import numpy as np

from space_invaders.animation import Animation


def test_animation():
    first = np.ones((5, 5))
    second = np.zeros((5, 5))
    a = Animation([first, second])
    assert (a.sprite() == first).all()
    assert (a.next() == second).all()
    assert (a.sprite() == second).all()
