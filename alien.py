import assets
import game_object
import game_settings
import player_bullet
from animation import Animation
from explosion import Explosion
from point import Point


class Alien(game_object.GameObject):
    def __init__(self, game, coords):
        self._alive = True
        self._coords = coords
        self._position = Point(
            24 + coords.x * 16,
            game_settings.alien_initial_y(game.round()) + coords.y * 16,
        )
        self._game = game
        alien_type = [0, 0, 1, 1, 2][coords.y]
        self._animation = Animation(assets.aliens()[alien_type])

    def alive(self):
        return self._alive

    def position(self):
        return self._position

    def sprite(self):
        return self._animation.sprite()

    def tick(self):
        pass

    def on_collision(self, other):
        if isinstance(other, player_bullet.PlayerBullet):
            self._game.spawn(
                Explosion(self._position, assets.alien_explosion(), 16)
            )
            self._alive = False
            self._game.add_score([10, 10, 20, 20, 30][self._coords.y])

    def move(self, velocity):
        self._position += velocity
        self._animation.next()

    def coords(self):
        return self._coords
