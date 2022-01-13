import system
import game_settings
import game_object
import assets
import util
from text_animation import TextAnimation
from text_object import TextObject, VariableTextObject
from point import Point


class Sprite(game_object.GameObject):
    def __init__(self, position, sprite):
        self._position = position
        self._sprite = sprite

    def alive(self):
        return True

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def tick(self):
        pass

    def on_collision(self, other):
        pass

class MenuSystem(system.System):
    def __init__(self, game):
        self._game = game
        self._y = 200
        self._delay = 5
        self._animations = []

    def tick(self):
        if len(self._animations) == 0:
            self._animations.append(TextAnimation(self._game, self._y, "PLAY", self._delay))
        elif not self._animations[-1].done_once():
            return
        elif len(self._animations) == 1:
            self._animations.append(TextAnimation(self._game, self._y, "SPACE INVADERS", self._delay))
        elif len(self._animations) == 2:
            text = "SCORE ADVANCE TABLE"
            self._padding = util.padding(text)
            self._y -= 16
            self._game.spawn(TextObject(Point(self._padding, self._y), text))
            self._y -= 16
            self._spawn_sprite(assets.saucer())
            self._animations.append(TextAnimation(self._game, self._y, "=? MYSTERY", self._delay))
        elif len(self._animations) in range(3, 6):
            i = len(self._animations)
            alien_type = 5 - i
            points = (6 - i) * 10
            self._spawn_sprite(assets.aliens()[alien_type][0])
            self._animations.append(TextAnimation(self._game, self._y, f"={points} POINTS", self._delay))
        self._game.spawn(self._animations[-1])
        self._y -= 16

    def _spawn_sprite(self, sprite):
        self._game.spawn(Sprite(Point(self._padding - sprite.shape[0] + 8 * len("SCORE"), self._y), sprite))
