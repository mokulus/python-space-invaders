from bullet import Bullet
from animation import Animation
from point import Point
from explosion import Explosion
from shield_system import Shield
import assets


class PlayerBullet(Bullet):
    def __init__(self, game, position):
        super().__init__(
            position,
            Animation([assets.player_shot()]),
            Point(0, 4),
        )
        self._game = game

    def on_collision(self, other):
        if isinstance(other, Explosion):
            return
        self._alive = False
        if isinstance(other, Shield):
            self._game.spawn(
                Explosion(
                    self._position + Point(-4, 2),
                    assets.player_shot_explosion(),
                    16,
                )
            )
