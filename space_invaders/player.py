"""
Provides :class:`Player`, :class:`Input`, :class:`DeathAnimation`,
:class:`GameOver`
"""
from enum import Flag

from space_invaders import assets, game_object
from space_invaders.alien_bullet import AlienBullet
from space_invaders.animation import Animation
from space_invaders.player_bullet import PlayerBullet
from space_invaders.point import Point
from space_invaders.text_animation import TextAnimation


class Input(Flag):
    """
    Set of flags that represent the possible actions of the `Player`.

    NONE - no action
    RIGHT - try to move right
    LEFT - try to move left
    SHOOT - try to fire a bullet
    """

    NONE = 0
    RIGHT = 1
    LEFT = 2
    SHOOT = 4


class GameOver(TextAnimation):
    """
    Represents the game over message. Resets the game when it ends.
    """

    def __init__(self, game):
        super().__init__(game, 200, "GAME OVER", 30)
        self.color = (255, 0, 0)

    def tick(self):
        super().tick()

        if self.done_once():
            self._game.reset()


class DeathAnimation(game_object.GameObject):
    """
    Represents the death animation of the player. Runs `reset_callback` if
    players still has lives left.
    """

    def __init__(self, game, reset_callback):
        """
        Initialize `DeathAnimation`. It will run `reset_callback` if player
        still has lives left when it ends.
        """
        super().__init__()
        self.color = (0, 255, 0)
        self._game = game
        self._animation = Animation(assets.player_explosion())
        self._countdown = 3 * 60 if self._game.player.lives() > 0 else 10 * 60
        self._reset_callback = reset_callback

    def position(self):
        return self._game.player.position()

    def sprite(self):
        return self._animation.sprite()

    def tick(self):
        if self._countdown % 10 == 0:
            self._animation.next()
        self._countdown -= 1
        if self._countdown == 0:
            self.alive = False
            if self._game.player.lives() > 0:
                self._reset_callback()


class Player(game_object.GameObject):
    """
    Represents the player.
    """

    def __init__(self, game):
        super().__init__()
        self.color = (0, 255, 0)
        self._game = game
        self._position = Point(0, 16)
        self._bullet = None
        self._shots_fired = 0
        self._lives = 3
        self._action = Input.NONE
        self._dying = False

    def position(self):
        return self._position

    def sprite(self):
        return assets.player() if not self._dying else assets.empty_sprite()

    def move_right(self):
        """
        Attempt to move the player right in the next tick.
        """
        self._action |= Input.RIGHT

    def move_left(self):
        """
        Attempt to move the player left in the next tick.
        """
        self._action |= Input.LEFT

    def _move(self, dx):
        if self._dying:
            return
        self._position.x += dx
        self._clamp_position()

    def _clamp_position(self):
        maxx = self._game.settings.width() - self.sprite().shape[0] - 1
        self._position.x = max(min(self._position.x, maxx), 0)

    def _reset(self):
        self._dying = False

    def shoot(self):
        """
        Attempt to shoot a bullet in the next tick.
        """
        self._action |= Input.SHOOT

    def shots_fired(self):
        """
        Return the total number of shots fired by the player.
        """
        return self._shots_fired

    def on_collision(self, other):
        if self._dying:
            return
        if (
            isinstance(other, AlienBullet)
            and not self._game.settings.invincibility()
        ):
            self._dying = True
            self._lives -= 1
            self._game.spawn(DeathAnimation(self._game, self._reset))
            if self._lives == 0:
                self._game.spawn(GameOver(self._game))

    def dying(self):
        """
        Check if player is dying.
        """
        return self._dying

    def tick(self):
        if self._bullet and not self._bullet.alive:
            self._bullet = None
        if not self._dying:
            if self._action & Input.RIGHT:
                self._move(1)
            if self._action & Input.LEFT:
                self._move(-1)
            if self._action & Input.SHOOT:
                if (
                    not self._bullet
                    or self._game.settings.infinite_bullets()
                    and self._game.ticks() % 2 == 0
                ):
                    self._shots_fired += 1
                    self._bullet = PlayerBullet(
                        self._game, self._position + Point(8, 0)
                    )
                    self._game.spawn(self._bullet)
        self._action = Input.NONE

    def lives(self):
        """
        Return the number of lives the player has left.
        """
        return self._lives

    def game_over(self):
        """
        End the game disregarding the number of lives the player has left. Used
        if the aliens get to close to the player.
        """
        self._dying = True
        self._game.spawn(DeathAnimation(self._game, self._reset))
        self._game.spawn(GameOver(self._game))
