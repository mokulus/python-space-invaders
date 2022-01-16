"""
Provides :class:`ShieldSystem`
"""
import numpy as np

from space_invaders import assets, system
from space_invaders.point import Point
from space_invaders.shield import Shield


class ShieldSystem(system.System):
    """
    Spawns the inital four main shields and the horizontal one.
    """

    def __init__(self, game):
        self._game = game
        shield_count = 4
        for i in range(shield_count):
            start = 32
            width = 22
            height = 40
            gap = (
                self._game.settings.width() - 2 * start - shield_count * width
            ) // (shield_count - 1)
            self._game.spawn(
                Shield(
                    self._game,
                    Point(start + (width + gap) * i, height),
                    assets.shield(),
                )
            )
        self._game.spawn(
            Shield(
                self._game,
                Point(0, 8),
                np.ones((self._game.settings.width(), 1), dtype=np.uint8),
            )
        )

    def tick(self):
        pass
