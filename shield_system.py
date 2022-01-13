import game_object
import game_settings
import assets
from point import Point
from explosion import Explosion
import alien_system
import util
import numpy as np
import system


class Shield(game_object.GameObject):
    def __init__(self, game, position, sprite):
        self._game = game
        self._position = position
        self._sprite = np.copy(sprite)

    def alive(self):
        return True

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def tick(self):
        pass

    def on_collision(self, other):
        if isinstance(other, Explosion) or isinstance(
            other, alien_system.Alien
        ):
            intersection_rect = util.intersection(
                self.position(),
                self.sprite(),
                other.position(),
                other.sprite(),
            )
            (minx, maxx), (miny, maxy) = intersection_rect
            sx = self.position()[0]
            sy = self.position()[1]
            if isinstance(other, alien_system.Alien):
                new_sprite = np.zeros_like(
                    util.sprite_view(other, intersection_rect)
                )
            else:
                inverted = np.logical_not(
                    util.sprite_view(other, intersection_rect)
                )
                new_sprite = np.logical_and(
                    util.sprite_view(self, intersection_rect), inverted
                )
            sprite = np.fliplr(self._sprite)
            sprite[minx - sx: maxx - sx, miny - sy: maxy - sy] = new_sprite
            self._sprite = np.fliplr(sprite)


class ShieldSystem(system.System):
    def __init__(self, game):
        self._game = game
        n = 4
        for i in range(n):
            # TODO are the values correct?
            start = 32
            width = 22
            y = 40
            gap = (game_settings.width() - 2 * start - n * width) // (n - 1)
            self._game.spawn(Shield(self._game, Point(
                start + (width + gap) * i, y), assets.shield()))
        self._game.spawn(
            Shield(
                self._game, Point(
                    0, 8), np.ones(
                    (game_settings.width(), 1), dtype=np.uint8)))

    def tick(self):
        pass
