from bullet import Bullet
from point import Point

class AlienBullet(Bullet):
    def __init__(self, position, animation, offset):
        super().__init__(position, animation, Point(0, -4))
        self._offset = offset
        self._ticks = 0

    def tick(self):
        if self._ticks % 3 == self._offset:
            super().tick()
        self._ticks += 1

    def on_collision(self, other):
        # TODO
        pass

