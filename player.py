from enum import Flag

import assets
import game_object
from alien_bullet import AlienBullet
from animation import Animation
from player_bullet import PlayerBullet
from point import Point
from text_animation import TextAnimation


class Input(Flag):
    NONE = 0
    RIGHT = 1
    LEFT = 2
    SHOOT = 4


class GameOver(TextAnimation):
    def __init__(self, game):
        super().__init__(game, 200, "GAME OVER", 30)

    def tick(self):
        super().tick()

        if self.done_once():
            self._game.reset()


class DeathAnimation(game_object.GameObject):
    def __init__(self, game):
        self._game = game
        self._animation = Animation(assets.player_explosion())
        self._countdown = 3 * 60 if self._game.player.lives() > 0 else 10 * 60

    def alive(self):
        return self._countdown > 0

    def position(self):
        return self._game.player.position()

    def sprite(self):
        return self._animation.sprite()

    def tick(self):
        if self._countdown % 10 == 0:
            self._animation.next()
        self._countdown -= 1
        if self._countdown == 0:
            if self._game.player._lives > 0:
                self._game.player._dying = False

    def on_collision(self, other):
        pass


class Player(game_object.GameObject):
    def __init__(self, game):
        self._alive = True
        self._game = game
        self._position = Point(0, 16)
        self._bullet = None
        self._shots_fired = 0
        self._lives = 3
        self._action = Input.NONE
        self._dying = False

    def alive(self):
        return self._alive

    def position(self):
        return self._position

    def sprite(self):
        return assets.player() if not self._dying else assets.empty_sprite()

    def move_right(self):
        self._action |= Input.RIGHT

    def move_left(self):
        self._action |= Input.LEFT

    def _move(self, dx):
        if self._dying:
            return
        self._position.x += dx
        self._clamp_position()

    def _clamp_position(self):
        maxx = self._game.settings.width() - self.sprite().shape[0] - 1
        self._position.x = max(min(self._position.x, maxx), 0)

    def shoot(self):
        self._action |= Input.SHOOT

    def shots_fired(self):
        return self._shots_fired

    def on_collision(self, other):
        if self._dying:
            return
        if isinstance(other, AlienBullet):
            self._dying = True
            self._lives -= 1
            self._game.spawn(DeathAnimation(self._game))
            if self._lives == 0:
                self._game.spawn(GameOver(self._game))

    def dying(self):
        return self._dying

    def tick(self):
        if self._bullet and not self._bullet.alive():
            self._bullet = None
        if not self._dying:
            if self._action & Input.RIGHT:
                self._move(1)
            if self._action & Input.LEFT:
                self._move(-1)
            if self._action & Input.SHOOT:
                if not self._bullet or self._game.settings.infinite_bullets():
                    self._shots_fired += 1
                    self._bullet = PlayerBullet(self._game, self._position + Point(8, 0))
                    self._game.spawn(self._bullet)
        self._action = Input.NONE

    def lives(self):
        return self._lives

    def game_over(self):
        self._dying = True
        self._game.spawn(DeathAnimation(self._game))
        self._game.spawn(GameOver(self._game))
