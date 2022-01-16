"""
Provides :class:`Bullet`
"""
from abc import abstractmethod

from space_invaders import game_object


class Bullet(game_object.GameObject):
    """
    Abstract bullet that explodes on collision or if out of bounds.
    """
    def __init__(self, game, position, animation, velocity):
        super().__init__()
        self._game = game
        self._position = position
        self._animation = animation
        self._velocity = velocity

    def position(self):
        return self._position

    def tick(self):
        self._position += self._velocity
        self._animation.next()

        if self._position.y <= self._game.settings.game_area_y_bounds()[0]:
            self.color = (0, 255, 0)
            self.explode()
        if self._position.y >= self._game.settings.game_area_y_bounds()[1]:
            self.color = (255, 0, 0)
            self.explode()

    def sprite(self):
        return self._animation.sprite()

    @abstractmethod
    def explode(self):
        """
        Kill the bullet and optionally spawn an `Explosion`. Bullet will
        explode if out of bounds.
        """
        self.alive = False
