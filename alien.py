from point import Point
from animation import Animation
import assets
import game_settings
import game_object
from explosion import Explosion
import player_bullet


class Alien(game_object.GameObject):
    def __init__(self, game, coords, alien_system):
        self._alive = True
        self._coords = coords
        self._alien_system = alien_system
        self._position = Point(
            24 + coords.x * 16,
            game_settings.alien_initial_y(game.round()) + coords.y * 16,
        )
        self._game = game
        self._animation = Alien._get_sprite(coords.y)

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

    @staticmethod
    def _get_sprite(y):
        alien_type = [0, 0, 1, 1, 2][y]
        return Animation(assets.aliens()[alien_type])