import game_object
import game_settings
import assets
from point import Point
from explosion import Explosion
import alien_system
import util
import numpy as np


class Shield(game_object.GameObject):
    def __init__(self, game, position):
        self._game = game
        self._position = position
        self._sprite = np.copy(assets.shield())

    def alive(self):
        return True

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def tick(self):
        pass

    def on_collision(self, other):
        if isinstance(other, Explosion):
            self._damage_explosion(other)
        elif isinstance(other, alien_system.Alien):
            # TODO
            pass

    def _damage_explosion(self, other):
        intersection_rect = util.intersection(self.position(), self.sprite(), other.position(), other.sprite())
        (minx, maxx), (miny, maxy) = intersection_rect
        ox = other.position()[0]
        oy = other.position()[1]
        sx = self.position()[0]
        sy = self.position()[1]

        inverted = np.logical_not(util.sprite_view(other, intersection_rect))
        removed = np.logical_and(util.sprite_view(self, intersection_rect), inverted)
        sprite = np.fliplr(self._sprite)
        sprite[minx - sx: maxx - sx, miny - sy: maxy - sy] = removed
        self._sprite = np.fliplr(sprite)

class ShieldSystem():
    def __init__(self, game):
        self._game = game
        n = 4
        for i in range(n):
            # TODO are the values correct?
            start = 32
            width = 22
            y = 24
            gap = (game_settings.width() - 2 * start - n * width) // (n - 1)
            self._game.spawn(Shield(self._game, Point(start + (width + gap) * i, y)))

    def tick():
        pass
