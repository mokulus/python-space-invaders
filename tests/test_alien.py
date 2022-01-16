import numpy as np

from space_invaders.explosion import Explosion
from space_invaders.point import Point


def test_alien_position(alien_factory):
    a = alien_factory(Point(0, 0))
    b = alien_factory(Point(1, 1))
    step = a.sprite().shape[0]
    assert b.position().x - a.position().x == step
    assert b.position().y - a.position().y == step


def test_alien_sprite(alien_factory):
    a = alien_factory()
    assert isinstance(a.sprite(), np.ndarray)


def test_alien_on_collision_explosion(
    game, alien_factory, player_bullet_factory
):
    a = alien_factory()
    pb = player_bullet_factory()
    a.on_collision(pb)
    assert isinstance(game.game_objects()[-1], Explosion)


def test_alien_on_collision_no_explosion(
    game, alien_factory, alien_bullet_factory
):
    a = alien_factory()
    ab = alien_bullet_factory()
    old_objects = list(game.game_objects())
    a.on_collision(ab)
    assert old_objects == game.game_objects()


def test_alien_move(alien_factory):
    a = alien_factory()
    start = a.position()
    start_sprite = a.sprite()
    velocity = Point(1, 1)
    a.move(velocity)
    assert start + velocity == a.position()
    assert (start_sprite != a.sprite()).any()


def test_alien_coord(alien_factory):
    coords = Point(2, 3)
    a = alien_factory(coords)
    assert a.coords() == coords
