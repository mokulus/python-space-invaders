import game_object
import assets
from point import Point
import player_bullet
import util
import game_settings
from explosion import Explosion
import system


class Saucer(game_object.GameObject):
    def __init__(self, game):
        self._game = game
        self._alive = True
        self._ticks = 0
        y = 208
        if game.player.shots_fired() % 2 == 0:
            self._position = Point(0, y)
            self._velocity = Point(2, 0)
        else:
            self._position = Point(
                game_settings.width() - self.sprite().shape[0] - 1, y
            )
            self._velocity = Point(-2, 0)

    def alive(self):
        return self._alive

    def position(self):
        return self._position

    def sprite(self):
        return assets.saucer()

    def tick(self):
        self._ticks += 1
        if self._ticks % 3 == 0:
            self._position += self._velocity
        if not util.inside(
            self._position.x,
            self.sprite().shape[0],
            game_settings.width(),
        ):
            self._alive = False

    def on_collision(self, other):
        if isinstance(other, player_bullet.PlayerBullet):
            self._game.spawn(
                Explosion(self._position, assets.saucer_explosion(), 60)
            )
            self._alive = False


class SaucerSystem(system.System):
    def __init__(self, game):
        self._game = game
        self._ticks = 0
        self._saucer = None

    def tick(self):
        if self._saucer is None or not self._saucer.alive():
            self._ticks += 1
            if self._ticks == 60:
                self._ticks = 0
                self._saucer = Saucer(self._game)
                self._game.spawn(self._saucer)
