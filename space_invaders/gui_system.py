"""
Provides :class:`GuiSystem`
"""
from space_invaders import system
from space_invaders.point import Point
from space_invaders.text_object import TextObject, VariableTextObject


class GuiSystem(system.System):
    """
    System that spawns game objects displaying score and highscore. Used both
    in menu and in game.
    """
    def __init__(self, game):
        self._game = game
        score_str = "SCORE<1>"
        hiscore_str = "HI-SCORE"
        ypad = 16
        letter_width = 8

        x = letter_width
        y = self._game.settings.height() - ypad
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
