from space_invaders.explosion import Explosion
from space_invaders.point import Point


def test_player_bullet_tick(game, player_bullet_factory):
    start = Point(0, 16)
    player_bullet = player_bullet_factory(position=start)
    game.spawn(player_bullet)
    game.tick()
    assert player_bullet.alive and player_bullet.position() != start


def test_player_bullet_explosion(game, player_bullet_factory, shield_factory):
    pb = player_bullet_factory()
    shield = shield_factory()
    pb.on_collision(shield)
    assert isinstance(game.game_objects()[-1], Explosion)


def test_player_bullet_no_explosion(game, player_bullet_factory):
    import space_invaders.player

    pb = player_bullet_factory()
    old_objects = list(game.game_objects())
    pb.on_collision(space_invaders.player.Player(game))
    assert old_objects == game.game_objects()
