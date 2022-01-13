import game_settings
from point import Point
import system
from text_object import TextObject, VariableTextObject


class GuiSystem(system.System):
    def __init__(self, game):
        self._game = game
        score_str = "SCORE<1>"
        hiscore_str = "HI-SCORE"
        ypad = 16
        letter_width = 8

        x = letter_width
        y = game_settings.height() - ypad
        self._game.spawn(TextObject(Point(x, y), score_str))

        x += 2 * letter_width
        y -= ypad
        self._game.spawn(
            VariableTextObject(
                self._game, Point(x, y), lambda g: f"{g.score():04}"
            )
        )
        x -= 2 * letter_width
        y += ypad

        x += letter_width * (len(score_str) + 1)
        self._game.spawn(TextObject(Point(x, y), hiscore_str))

        x += 2 * letter_width
        y -= ypad
        self._game.spawn(
            VariableTextObject(
                self._game, Point(x, y), lambda g: f"{g.highscore():04}"
            )
        )
        x -= 2 * letter_width
        y += ypad

        # x += letter_width * (len(hiscore_str) + 1)
        # self._game.spawn(TextObject(Point(x, y), score_str))

    def tick(self):
        pass
