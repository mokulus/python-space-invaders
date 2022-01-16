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
        self._alien_iter = iter(self._aliens)
        self._initialized = False

    def tick(self):
        if self._game.player.dying():
            return
        if not any(alien.alive for alien in self._aliens):
            self._game.next_round()
            return
        if any(
            alien.position().y == self._game.player.position().y
            for alien in self._aliens
            if alien.alive
        ):
            self._game.player.game_over()
            return
        if not self._initialized:
            self._init_animation()
            return
        self._alien_iter = (
            alien for alien in self._alien_iter if alien.alive
        )
        next_alien = next(self._alien_iter, None)
        if next_alien:
            next_alien.move(self._velocity)
        else:
            self._alien_iter = iter(self._aliens)
            aminx = min(
                (alien.position().x for alien in self._aliens if alien.alive)
            )
            amaxx = max(
                (alien.position().x for alien in self._aliens if alien.alive)
            )
            minx = 0
            maxx = (
                self._game.settings.width() - assets.aliens()[0][0].shape[0]
            )
            if aminx == minx or amaxx == maxx:
                if self._velocity.y == 0:
                    self._velocity.x = 0
                    self._velocity.y = -8
                else:
                    self._velocity.x = 2 if aminx == minx else -2
                    self._velocity.y = 0

    def _init_animation(self):
        if self._game.ticks() % 2 != 0:
            return
        alien = next(self._alien_iter, None)
        if not alien:
            self._initialized = True
            self._alien_iter = iter(self._aliens)
            self._game.spawn(self._game.player)
            self._game.add_system(BulletSystem(self._game, self))
            self._game.add_system(SaucerSystem(self._game))
        else:
            self._game.spawn(alien)

    def aliens(self):
        """
        Return a list of all aliens initially spawned, even if dead.
        """
        return self._aliens
