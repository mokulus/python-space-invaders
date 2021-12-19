from bullet import Bullet
from animation import Animation
from point import Point
from alien_grid import Alien
import assets


class PlayerBullet(Bullet):
    def __init__(self, position):
        super().__init__(
            position,
            Animation([assets.load_player_shot()]),
            Point(0, 4),
        )

    def on_collision(self, other):
        if isinstance(other, Alien):
            self._alive = False
