"""
Provides :class:`MenuSystem`
"""
from space_invaders import assets, system, util
from space_invaders.point import Point
from space_invaders.static_sprite import StaticSprite
from space_invaders.text_animation import TextAnimation
from space_invaders.text_object import TextObject


class MenuSystem(system.System):
    """
    `System` that spawns animations in the main menu.
    """

    def __init__(self, game):
        self._game = game
        self._y = 192
        self._delay = 5
        self._padding = 0
        self._animations = []

    def tick(self):
        if len(self._animations) == 0:
            self._animations.append(
                TextAnimation(self._game, self._y, "PLAY", self._delay)
            )
            self._y -= 16
        elif not self._animations[-1].done_once():
            return
        elif len(self._animations) == 1:
            self._animations.append(
                TextAnimation(
                    self._game, self._y, "SPACE INVADERS", self._delay
                )
            )
        elif len(self._animations) == 2:
            text = "SCORE ADVANCE TABLE"
            self._padding = util.padding(self._game.settings.width(), text)
            self._y -= 16
            self._game.spawn(TextObject(Point(self._padding, self._y), text))
            self._y -= 16
            self._spawn_sprite(assets.saucer())
            self._animations.append(
                TextAnimation(self._game, self._y, "=? MYSTERY", self._delay)
            )
        elif len(self._animations) in range(3, 6):
            i = len(self._animations)
            alien_type = 5 - i
            points = (6 - i) * 10
            self._spawn_sprite(assets.aliens()[alien_type][0])
            self._animations.append(
                TextAnimation(
                    self._game, self._y, f"={points} POINTS", self._delay
                )
            )
        self._game.spawn(self._animations[-1])
        self._y -= 16

    def _spawn_sprite(self, sprite):
        self._game.spawn(
            StaticSprite(
                Point(
                    self._padding - sprite.shape[0] + 8 * len("SCORE"),
                    self._y,
                ),
                sprite,
            )
        )
