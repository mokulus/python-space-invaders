"""
Provides :class:`AlienSystem`
"""
from space_invaders import assets, system
from space_invaders.alien import Alien
from space_invaders.bullet_system import BulletSystem
from space_invaders.point import Point
from space_invaders.saucer_system import SaucerSystem


class AlienSystem(system.System):
    """
    `System` that manages the aliens. It does the initial alien animation and
    decides which alien to move in the current frame.
    """

    def __init__(self, game):
        self._game = game
        self._aliens = []
        self._velocity = Point(2, 0)
        for y in range(5):
            for x in range(11):
                alien = Alien(self._game, Point(x, y))
                self._aliens.append(alien)
        self._alien_iter = self._make_alien_iter()
        self._initialized = False

    def tick(self):
        if self._game.player.dying():
            return
        self._aliens = [alien for alien in self._aliens if alien.alive]
        if not self._aliens:
            self._game.next_round()
            return
        if any(
            alien.position().y == self._game.player.position().y
            for alien in self._aliens
        ):
            self._game.player.game_over()
            return
        if not self._initialized:
            self._init_animation()
            return
        alien = next(self._alien_iter, None)
        if alien:
            alien.move(self._velocity)
        else:
            self._alien_iter = self._make_alien_iter()
            aliens_max_pos_x = max(
                (alien.position().x for alien in self._aliens)
            )
            aliens_min_pos_x = min(
                (alien.position().x for alien in self._aliens)
            )
            min_x_allowed = 0
            max_x_allowed = (
                self._game.settings.width() - assets.aliens()[0][0].shape[0]
            )
            at_left_edge = aliens_min_pos_x == min_x_allowed
            at_right_edge = aliens_max_pos_x == max_x_allowed
            if at_left_edge or at_right_edge:
                if self._velocity.y == 0:
                    self._velocity.x = 0
                    self._velocity.y = -8
                else:
                    self._velocity.x = 2 if at_left_edge else -2
                    self._velocity.y = 0

    def _init_animation(self):
        if self._game.ticks() % 2 != 0:
            return
        alien = next(self._alien_iter, None)
        if not alien:
            self._initialized = True
            self._alien_iter = self._make_alien_iter()
            self._game.spawn(self._game.player)
            self._game.add_system(BulletSystem(self._game, self))
            self._game.add_system(SaucerSystem(self._game))
        else:
            self._game.spawn(alien)

    def _make_alien_iter(self):
        return iter(alien for alien in self._aliens if alien.alive)

    def aliens(self):
        """
        Return a list of all alive aliens.
        """
        return self._aliens
