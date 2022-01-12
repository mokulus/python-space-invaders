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


class VariableTextObject(TextObject):
    def __init__(self, game, position, text_getter):
        self._game = game
        self._text_getter = text_getter
        super().__init__(position, self._text_getter(self._game))

    def tick(self):
        self.set_text(self._text_getter(self._game))


class GuiSystem:

    def __init__(self, game):
        self._game = game
        score_str = "SCORE<1>"
        hiscore_str = "HI-SCORE"
        padding = 16
        letter_width = 8

        x = letter_width
        y = game_settings.height() - padding
        self._game.spawn(TextObject(Point(x, y), score_str))

        x += 2 * letter_width
        y -= padding
        self._game.spawn(VariableTextObject(self._game, Point(x, y), lambda g: f"{g.score():04}"))
        x -= 2 * letter_width
        y += padding

        x += letter_width * (len(score_str) + 1)
        self._game.spawn(TextObject(Point(x, y), hiscore_str))

        x += 2 * letter_width
        y -= padding
        self._game.spawn(VariableTextObject(self._game, Point(x, y), lambda g: f"{g.highscore():04}"))
        x -= 2 * letter_width
        y += padding

        # x += letter_width * (len(hiscore_str) + 1)
        # self._game.spawn(TextObject(Point(x, y), score_str))

    def tick(self):
        pass
