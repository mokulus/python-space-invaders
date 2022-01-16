import numpy as np

from space_invaders import alien_system, game_object, util
from space_invaders.explosion import Explosion


class Shield(game_object.GameObject):
    def __init__(self, game, position, sprite):
        super().__init__()
        self.color = (0, 255, 0)
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
