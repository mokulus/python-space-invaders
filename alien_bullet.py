from bullet import Bullet
from point import Point
from explosion import Explosion
import shield_system
import assets

class AlienBullet(Bullet):
    def __init__(self, game, position, animation, offset):
        super().__init__(position, animation, Point(0, -4))
        self._offset = offset
        self._ticks = 0
        self._game = game

    def tick(self):
        if self._ticks % 3 == self._offset:
            super().tick()
        self._ticks += 1

    def on_collision(self, other):
        self._alive = False
        # TODO more?
        if isinstance(other, shield_system.Shield) or isinstance(other, Bullet):
            self._game.spawn(Explosion(self._position + Point(-2, 0), assets.alien_shot_explosion(), 16))

