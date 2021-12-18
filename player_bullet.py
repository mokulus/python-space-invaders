from bullet import Bullet
from animation import Animation
from point import Point
import assets


class PlayerBullet(Bullet):
    def __init__(self, game, position):
        super().__init__(
            game,
            position,
            Animation([assets.load_player_shot()]),
            Point(0, 4),
        )

    def on_collision(self, other):
        pass
