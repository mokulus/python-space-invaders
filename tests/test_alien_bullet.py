from space_invaders.explosion import Explosion
from space_invaders.point import Point


def test_alien_bullet_tick(game, alien_bullet_factory):
    start = Point(0, 16)
    ab = alien_bullet_factory(position=start)
    game.spawn(ab)
    for _ in range(3):
        game.tick()
    assert ab.alive and ab.position() != start


def test_alien_bullet_explosion(
    game, alien_bullet_factory, player_bullet_factory
):
    ab = alien_bullet_factory()
    pb = player_bullet_factory()
    ab.on_collision(pb)
    assert isinstance(game.game_objects()[-1], Explosion)


def test_alien_bullet_no_explosion(game, alien_bullet_factory, alien_factory):
    ab = alien_bullet_factory()
    a = alien_factory()
    old_objects = list(game.game_objects())
    ab.on_collision(a)
    assert old_objects == game.game_objects()
