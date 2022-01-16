"""
Provides :class:`StaticSprite`
"""
from space_invaders import game_object


class StaticSprite(game_object.GameObject):
    """
    Simple object that only displays a sprite.
    """

    def __init__(self, position, sprite):
        super().__init__()
        self._position = position
        self._sprite = sprite

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite
