from bullet import Bullet
from point import Point
from explosion import Explosion
import assets
from alien import Alien


class AlienBullet(Bullet):
    def __init__(self, game, position, animation):
        super().__init__(position, animation, Point(0, -4))
        self._ticks = 0
        self._game = game

    def tick(self):
        if self._ticks % 3 == 0:
            super().tick()
        self._ticks += 1
        if self._position.y == 8:
            self._explode()

    def on_collision(self, other):
        if not isinstance(other, Explosion) and not isinstance(other, Alien):
            self._explode()

    def _explode(self):
        self._game.spawn(
            Explosion(
                self._position + Point(-2, 0),
                assets.alien_shot_explosion(),
                16,
            )
        )
        self._alive = False
