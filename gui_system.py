import game_object
import assets
import numpy as np
import game_settings
from point import Point


def text_to_sprite(str):
    sprite = np.zeros((8 * len(str), 8), dtype=np.uint8)
    font = assets.font()
    font_characters = assets.font_characters()
    for i in range(len(str)):
        sprite[8 * i:8 * (i + 1), :] = font[font_characters.index(str[i])]
    return sprite

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
        self._sprite = text_to_sprite(text)

    def text(self):
        return self._text

    def tick(self):
        pass

    def on_collision(self, other):
        pass

class ScoreTextObject(TextObject):
    def __init__(self, game, position, text):
        self._game = game
        super().__init__(position, text)

    def tick(self):
        self.set_text(f"{self._game.score():04}")


class GuiSystem:

    def __init__(self, game):
        self._game = game
        self._game.spawn(TextObject(Point(16, game_settings.height() - 16), "SCORE<1>"))
        self._game.spawn(ScoreTextObject(self._game, Point(32, game_settings.height() - 16 - 16), ""))

    def tick(self):
        pass
