import game_object
import assets
import numpy as np
import util


class TextObject(game_object.GameObject):
    def __init__(self, position, text):
        self._position = position
        self.set_text(text)

    def alive(self):
        return True

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def set_text(self, text):
        self._text = text
        self._sprite = util.text_to_sprite(text)

    def text(self):
        return self._text

    def tick(self):
        pass

    def on_collision(self, other):
        pass


class VariableTextObject(TextObject):
    def __init__(self, game, position, text_getter):
        self._game = game
        self._text_getter = text_getter
        super().__init__(position, self._text_getter(self._game))

    def tick(self):
        self.set_text(self._text_getter(self._game))


