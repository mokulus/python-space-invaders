import assets
from animation import Animation
from bullet import Bullet
from explosion import Explosion
from point import Point
from shield_system import Shield


class PlayerBullet(Bullet):
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
        self._alive = False
        if isinstance(other, Shield):
            self.explode()

    def explode(self):
        super().explode()
        self._game.spawn(
            Explosion(
                self._position + Point(-4, 2),
                assets.player_shot_explosion(),
                16,
            )
        )
