from bullet import Bullet
from point import Point
from explosion import Explosion
import shield_system
import assets


class AlienBullet(Bullet):
    def __init__(self, game, position, animation):
        super().__init__(position, animation, Point(0, -4))
        self._ticks = 0
        self._game = game

    def tick(self):
        if self._ticks % 3 == 0:
            super().tick()
        self._ticks += 1

    def on_collision(self, other):
        if isinstance(other, shield_system.Shield) or isinstance(
            other, Bullet
        ):
            self._game.spawn(
                Explosion(
                    self._position + Point(-2, 0),
                    assets.alien_shot_explosion(),
                    16,
                )
            )
            self._alive = False
