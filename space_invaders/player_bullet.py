"""
Provides :class:`PlayerBullet`
"""
from space_invaders import assets
from space_invaders.animation import Animation
from space_invaders.bullet import Bullet
from space_invaders.explosion import Explosion
from space_invaders.point import Point
from space_invaders.shield import Shield


class PlayerBullet(Bullet):
    """
    Bullet shot by the player. Explodes only when hitting shields.
    """

    def __init__(self, game, position):
        super().__init__(
            game,
            position,
            Animation([assets.player_shot()]),
            Point(0, 4),
        )

    def on_collision(self, other):
        if isinstance(other, Explosion):
            return
        self.alive = False
        self.color = other.color
        if isinstance(other, Shield):
            self.explode()

    def explode(self):
        super().explode()
        pos = self._position + Point(-4, 2)
        sprite = assets.player_shot_explosion()
        obj = Explosion(pos, sprite, self.color, 16)
        self._game.spawn(obj)
