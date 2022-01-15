from space_invaders import assets
from space_invaders.alien import Alien
from space_invaders.bullet import Bullet
from space_invaders.explosion import Explosion
from space_invaders.point import Point


class AlienBullet(Bullet):
    def __init__(self, game, position, animation):
        super().__init__(game, position, animation, Point(0, -4))

    def tick(self):
        if self._game.ticks() % 3 == 0:
            super().tick()

    def on_collision(self, other):
        if not isinstance(other, (Explosion, Alien)):
            self.explode()

    def explode(self):
        super().explode()
        self._game.spawn(
            Explosion(
                self._position + Point(-2, 0),
                assets.alien_shot_explosion(),
                16,
            )
        )
        self._alive = False
