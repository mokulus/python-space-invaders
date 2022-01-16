from space_invaders import assets, game_object, player_bullet
from space_invaders.animation import Animation
from space_invaders.explosion import Explosion
from space_invaders.point import Point


class Alien(game_object.GameObject):
    def __init__(self, game, coords):
        super().__init__()
        self._coords = coords
        self._position = Point(
            24 + coords.x * 16,
            game.settings.alien_initial_y() + coords.y * 16,
        )
        self._game = game
        alien_type = [0, 0, 1, 1, 2][coords.y]
        self._animation = Animation(assets.aliens()[alien_type])

    def position(self):
        return self._position

    def sprite(self):
        return self._animation.sprite()

    def on_collision(self, other):
        if isinstance(other, player_bullet.PlayerBullet):
            self._game.spawn(
                Explosion(
                    self._position, assets.alien_explosion(), self.color, 16
                )
            )
            self.alive = False
            self._game.add_score([10, 10, 20, 20, 30][self._coords.y])

    def move(self, velocity):
        self._position += velocity
        self._animation.next()

    def coords(self):
        return self._coords
