import assets
import game_settings
from point import Point
from player_bullet import PlayerBullet
from alien_bullet import AlienBullet
from animation import Animation
from game_over import GameOver
import game_object
from enum import Enum


class Input(Enum):
    RIGHT = 1
    LEFT = 2
    SHOOT = 3


class Player(game_object.GameObject):
    def __init__(self, game):
        self._alive = True
        self._game = game
        self._position = Point(0, 16)
        self._shots_fired = 0
        self._lives = 3
        self._action = None
        self._reset()

    def alive(self):
        return self._alive

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def move_right(self):
        self._action = Input.RIGHT

    def move_left(self):
        self._action = Input.LEFT

    def _move(self, dx):
        if self._dying:
            return
        self._position.x += dx
        self._clamp_position()

    def _clamp_position(self):
        maxx = game_settings.width() - self._sprite.shape[0] - 1
        self._position.x = max(min(self._position.x, maxx), 0)

    def shoot(self):
        self._action = Input.SHOOT

    def shots_fired(self):
        return self._shots_fired

    def on_collision(self, other):
        if self._dying:
            return
        if isinstance(other, AlienBullet):
            self._dying = True
            self._sprite = self._death_animation.sprite()
            if self._lives == 1:
                self._game.spawn(GameOver(self._game))

    def _reset(self):
        self._dying = False
        self._dying_length = 3 * 60
        self._death_animation = Animation(assets.player_explosion())
        self._sprite = assets.player()

    def dying(self):
        return self._dying

    def tick(self):
        if self._dying:
            if self._dying_length % 10 == 0:
                self._sprite = self._death_animation.next()
            self._dying_length -= 1
            if self._dying_length == 0:
                self._lives -= 1
                if self._lives > 0:
                    self._reset()
        else:
            if self._action == Input.RIGHT:
                self._move(1)
            elif self._action == Input.LEFT:
                self._move(-1)
            elif self._action == Input.SHOOT:
                self._shots_fired += 1
                self._game.spawn(
                    PlayerBullet(self._game, self._position + Point(8, 4))
                )
            self._action = None

    def lives(self):
        return self._lives
