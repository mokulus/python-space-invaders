import assets
import game_settings
from point import Point
from player_bullet import PlayerBullet
import game_object


class Player(game_object.GameObject):
    def __init__(self, game):
        self.game = game
        self._sprite = assets.load_player()
        self.position = Point()

    def sprite(self):
        return self._sprite

    def move_right(self):
        self._move(1)

    def move_left(self):
        self._move(-1)

    def _move(self, dx):
        self.position.x += dx
        self._clamp_position()

    def _clamp_position(self):
        maxx = game_settings.width() - self._sprite.shape[0] - 1
        self.position.x = max(min(self.position.x, maxx), 0)

    def shoot(self):
        self.game.bullets.append(
            PlayerBullet(self.game, self.position + Point(8, 8))
        )

    def on_collision(self, other):
        # TODO
        pass

    def tick(self):
        # TODO
        pass
