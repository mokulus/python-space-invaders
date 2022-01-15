import numpy as np

from space_invaders import alien_system, assets, game_object, system, util
from space_invaders.explosion import Explosion
from space_invaders.point import Point


class Shield(game_object.GameObject):
    def __init__(self, game, position, sprite):
        super().__init__()
        self._game = game
        self._position = position
        self._sprite = np.copy(sprite)

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def on_collision(self, other):
        if isinstance(other, (Explosion, alien_system.Alien)):
            intersection_rect = util.intersection(
                self.position(),
                self.sprite(),
                other.position(),
                other.sprite(),
            )
            (minx, maxx), (miny, maxy) = intersection_rect
            self_x = self.position()[0]
            self_y = self.position()[1]
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
            sprite[
                minx - self_x : maxx - self_x, miny - self_y : maxy - self_y
            ] = new_sprite
            self._sprite = np.fliplr(sprite)


class ShieldSystem(system.System):
    def __init__(self, game):
        self._game = game
        shield_count = 4
        for i in range(shield_count):
            start = 32
            width = 22
            height = 40
            gap = (
                self._game.settings.width() - 2 * start - shield_count * width
            ) // (shield_count - 1)
            self._game.spawn(
                Shield(
                    self._game,
                    Point(start + (width + gap) * i, height),
                    assets.shield(),
                )
            )
        self._game.spawn(
            Shield(
                self._game,
                Point(0, 8),
                np.ones((self._game.settings.width(), 1), dtype=np.uint8),
            )
        )

    def tick(self):
        pass
