"""
Provides :class:`BulletSystem`
"""
import itertools

from space_invaders import assets, system
from space_invaders.alien_bullet import AlienBullet
from space_invaders.animation import Animation
from space_invaders.point import Point


class BulletSystem(system.System):
    """
    `System` that spawns bullets. Ensures there is at least one bullet spawned,
    keeps track of spawn tables and cycling of bullet types.
    """

    def __init__(self, game, alien_system):
        self._game = game
        self._alien_system = alien_system
        self._fire_delay = 0
        self._index = 0

        self._bullets = []

        for i in range(3):
            self._bullets.append(
                AlienBullet(
                    self._game,
                    Point(),
                    Animation(assets.alien_shots()[i]),
                )
            )

        self._spawn_tables = []
        self._spawn_tables.append(None)
        self._spawn_tables.append(
            itertools.cycle(self._game.settings.plunger_shot_spawn_table())
        )
        self._spawn_tables.append(
            itertools.cycle(self._game.settings.squiggly_shot_spawn_table())
        )

        for bullet in self._bullets:
            bullet.alive = False

    def tick(self):
        if self._game.player.dying():
            return
        self._fire_delay += 1
        bullet = self._bullets[self._index]
        spawn_table = self._spawn_tables[self._index]
        if not bullet.alive:
            if (
                not any(bullet.alive for bullet in self._bullets)
                or self._fire_delay >= self._game.settings.alien_fire_period()
            ):
                if spawn_table:
                    x = next(spawn_table) - 1
                    alien = next(
                        (
                            alien
                            for alien in self._alien_system.aliens()
                            if alien.coords().x == x
                        ),
                        None,
                    )
                else:  # aiming shot
                    x = self._game.player.position().x // 16
                    alien = next(
                        (
                            alien
                            for alien in self._alien_system.aliens()
                            if alien.position().x // 16 == x
                        ),
                        None,
                    )
                if alien:
                    self._fire_delay = 0
                    self._bullets[self._index] = AlienBullet(
                        self._game,
                        alien.position() + Point(8, 0),
                        Animation(assets.alien_shots()[self._index]),
                    )
                    self._game.spawn(self._bullets[self._index])
                self._index += 1
                self._index %= len(self._bullets)
