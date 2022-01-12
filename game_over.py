from point import Point
import util
import game_object
import game_settings

class GameOver(game_object.GameObject):
    def __init__(self, game):
        self._game = game
        self._text = "GAME OVER"
        self._ticks = 0
        self._sprite = util.text_to_sprite(self._text[0])

    def alive(self):
        return True

    def position(self):
        text_width = len(self._text) * 8
        padding = (game_settings.width() - text_width) // 2
        return Point(padding, 200)

    def sprite(self):
        return self._sprite

    def tick(self):
        self._ticks += 1
        period = 30
        self._sprite = util.text_to_sprite(self._text[:1 + self._ticks // period])

        if len(self._text) * period == self._ticks:
            self._game.reset()

    def on_collision(self, other):
        pass
