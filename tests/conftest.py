import pytest


@pytest.fixture()
def game():
    from space_invaders.game import Game

    return Game(False)


@pytest.fixture
def alien_factory(game):
    from space_invaders.alien import Alien
    from space_invaders.point import Point

    def create(coords=Point()):
        return Alien(game, coords)

    return create


@pytest.fixture
def alien_bullet_factory(game):
    from space_invaders import assets
    from space_invaders.alien_bullet import AlienBullet
    from space_invaders.animation import Animation
    from space_invaders.point import Point

    def create(position=Point(), animation=None):
        if animation is None:
            animation = Animation(assets.alien_shots()[0])
        return AlienBullet(game, position, animation)

    return create


@pytest.fixture
def player_bullet_factory(game):
    from space_invaders.player_bullet import PlayerBullet
    from space_invaders.point import Point

    def create(position=Point()):
        return PlayerBullet(game, position)

    return create


@pytest.fixture
def shield_factory(game):
    from space_invaders import assets
    from space_invaders.point import Point
    from space_invaders.shield import Shield

    def create(position=Point(), sprite=None):
        if sprite is None:
            sprite = assets.shield()
        return Shield(game, position, sprite)

    return create
