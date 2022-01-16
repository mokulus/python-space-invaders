"""
Provides :class:`Explosion`
"""
from space_invaders import game_object


class Explosion(game_object.GameObject):
    """
    Sprite that will destroy itself after `frames` ticks pass.
    """
    def __init__(self, position, sprite, color, frames):
        super().__init__()
        self.color = color
        self._position = position
        self._sprite = sprite
        self._frames = frames

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def tick(self):
        self._frames -= 1
        if self._frames <= 0:
            self.alive = False
