"""
Provides :class:`Animation`
"""
import itertools


class Animation:
    """
    Cycles through an interator of sprites, which represents a looped
    animation.
    """
    def __init__(self, sprites):
        self._sprites = itertools.cycle(iter(sprites))
        self.next()

    def sprite(self):
        """
        Return current sprite in animation.
        """
        return self._current_sprite

    def next(self):
        """
        Move to next frame and return new sprite.
        """
        self._current_sprite = next(self._sprites)
        return self.sprite()
