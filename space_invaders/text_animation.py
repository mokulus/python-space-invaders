"""
Provides :class:`TextAnimation`
"""
from space_invaders import game_object, util
from space_invaders.point import Point


class TextAnimation(game_object.GameObject):
    """
    `GameObject` that animates the text. Every letter is shown every `delay` frames.
    """
    def __init__(self, game, y, text, delay):
        super().__init__()
        self._game = game
        self._text = text
        self._ticks = 0
        self._delay = delay
        self._y = y
        self._sprite = util.text_to_sprite(self._text[0])

    def position(self):
        return Point(
            util.padding(self._game.settings.width(), self._text), self._y
        )

    def sprite(self):
        return self._sprite

    def tick(self):
        self._ticks += 1
        self._sprite = util.text_to_sprite(
            self._text[: 1 + self._ticks // self._delay]
        )

    def done_once(self):
        """
        Check if current frame is the one in which the animation finished.
        Return True only in this frame.
        """
        return len(self._text) * self._delay == self._ticks
