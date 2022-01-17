"""
Provides :class:`AlienBullet`
"""
from space_invaders import assets
from space_invaders.alien import Alien
from space_invaders.bullet import Bullet
from space_invaders.explosion import Explosion
from space_invaders.point import Point


class AlienBullet(Bullet):
    """
    Bullet shot by the aliens. Will explode with anything.
    """

    def __init__(self, game, position, animation):
        super().__init__(game, position, animation, Point(0, -4))

    def tick(self):
        if self._game.ticks() % 3 == 0:
            super().tick()

    def on_collision(self, other):
        if not isinstance(other, (Explosion, Alien)):
            self.color = other.color
            self.explode()

    def explode(self):
        super().explode()
        pos = self._position + Point(-2, 0)
        sprite = assets.alien_shot_explosion()
        obj = Explosion(pos, sprite, self.color, 16)
        self._game.spawn(obj)
