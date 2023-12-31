"""
Provides :class:`TextObject` and :class:`VariableTextObject`
"""
from space_invaders import util
from space_invaders.static_sprite import StaticSprite


class TextObject(StaticSprite):
    """
    `StaticSprite` that displays text.
    """

    def __init__(self, position, text):
        super().__init__(position, None)
        self.set_text(text)

    def set_text(self, text):
        """
        Set displayed text to `text`.
        """
        self._text = text
        self._sprite = util.text_to_sprite(text)

    def text(self):
        """
        Return currently displayed text.
        """
        return self._text


class VariableTextObject(TextObject):
    """
    `TextObject` that updates it's text via callback every frame. The callback
    takes `Game` object and returns a string.
    """

    def __init__(self, game, position, text_getter):
        self._game = game
        self._text_getter = text_getter
        super().__init__(position, self._text_getter(self._game))

    def tick(self):
        self.set_text(self._text_getter(self._game))
