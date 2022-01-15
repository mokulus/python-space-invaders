from space_invaders import game_object, util
from space_invaders.point import Point


class TextAnimation(game_object.GameObject):
    def __init__(self, game, y, text, delay):
        self._game = game
        self._text = text
        self._ticks = 0
        self._delay = delay
        self._y = y
        self._sprite = util.text_to_sprite(self._text[0])

    def alive(self):
        return True

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
        return len(self._text) * self._delay == self._ticks

    def on_collision(self, other):
        pass
