from alien_bullet import AlienBullet
from point import Point
from animation import Animation
import assets
import game_settings
import itertools
import system


class BulletSystem(system.System):
    def __init__(self, game, alien_system):
        self._game = game
        self._alien_system = alien_system
        self._fire_delay = 0
        self._index = 0

        self._bullets = []

        for i in range(3):
            self._bullets.append(
                AlienBullet(
                    self._game, Point(), Animation(assets.alien_shots()[i]),
                )
            )

        self._spawn_tables = []
        self._spawn_tables.append(None)
        self._spawn_tables.append(
            itertools.cycle(game_settings.plunger_shot_spawn_table())
        )
        self._spawn_tables.append(
            itertools.cycle(game_settings.squiggly_shot_spawn_table())
        )

        for bullet in self._bullets:
            bullet._alive = False

    def tick(self):
        if not self._alien_system.initialized():
            return
        self._fire_delay += 1
        bullet = self._bullets[self._index]
        spawn_table = self._spawn_tables[self._index]
        if not bullet.alive():
            # TODO score?
            if not any(
                bullet.alive() for bullet in self._bullets
            ) or self._fire_delay >= game_settings.alien_fire_period(
                self._game.score()
            ):
                if spawn_table:
                    x = next(spawn_table) - 1
                else:  # aiming shot
                    playerx = self._game.player.position().x
                    x = (playerx - 24 - self._alien_system.delta().x) // 16
                alien = next(
                    (
                        alien
                        for alien in self._alien_system.aliens()
                        if alien.alive() and alien.coords().x == x
                    ),
                    None,
                )
                if alien:
                    self._fire_delay = 0
                    self._bullets[self._index] = AlienBullet(
                        self._game,
                        alien.position() + Point(8, -8),
                        Animation(assets.alien_shots()[self._index]),
                    )
                    self._game.spawn(self._bullets[self._index])
                self._index += 1
                self._index %= len(self._bullets)
