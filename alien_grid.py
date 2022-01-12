from point import Point
from animation import Animation
import assets
import game_settings
from dataclasses import dataclass
import game_object
from explosion import Explosion
from bullet import Bullet
import itertools


@dataclass
class Alien(game_object.GameObject):
    def __init__(self, game, coords, alien_grid):
        self._alive = True
        self._coords = coords
        self._alien_grid = alien_grid
        self._position = Point(24 + coords.x * 16, 120 + coords.y * 16)
        self._game = game
        self._animation = Alien._get_sprite(coords.y)

    def alive(self):
        return self._alive

    def position(self):
        return self._position

    def sprite(self):
        return self._animation.sprite()

    def tick(self):
        pass

    def on_collision(self, other):
        if isinstance(other, Bullet):
            self._game.spawn(
                Explosion(self._position, assets.alien_explosion(), 16)
            )
            self._alive = False

    def move(self, velocity):
        self._position += velocity
        self._animation.next()

    @staticmethod
    def _get_sprite(y):
        alien_type = [0, 0, 1, 1, 2][y]
        return Animation(assets.aliens()[alien_type])


class AlienBullet(Bullet):
    def __init__(self, position, animation, offset):
        super().__init__(position, animation, Point(0, -4))
        self._offset = offset
        self._ticks = 0

    def tick(self):
        # FIXME order?
        self._ticks += 1
        if self._ticks % 3 == self._offset:
            super().tick()

    def on_collision(self, other):
        # TODO
        pass

class AlienGrid:
    def __init__(self, game):
        self._game = game
        self._aliens = []
        self._delta = Point()
        self._velocity = Point(2, 0)
        for y in range(5):
            for x in range(11):
                alien = Alien(self._game, Point(x, y), self)
                self._aliens.append(alien)
                self._game.spawn(alien)
        self._alien_iter = iter(self._aliens)
        self._bullet_system = BulletSystem(game, self)

    def tick(self):
        self._alien_iter = (
            alien for alien in self._alien_iter if alien.alive()
        )
        next_alien = next(self._alien_iter, None)
        if next_alien:
            next_alien.move(self._velocity)
        else:
            self._alien_iter = iter(self._aliens)
            self._delta += self._velocity
            if self._delta.x == 24:
                self._velocity.x *= -1
            if self._delta.x == -24:
                if self._velocity.y == 0:
                    self._velocity.x = 0
                    self._velocity.y = -8
                else:
                    self._velocity.x = 2
                    self._velocity.y = 0
        self._bullet_system.tick(self._aliens)

    def alien_count(self):
        return sum(alien.alive for alien in self._aliens)

class BulletSystem:
    def __init__(self, game, alien_grid):
        self._game = game
        self._alien_grid = alien_grid
        self._bullets = []
        self._spawn_tables = []
        self._to_shoot = 0

        for i in range(3):
            self._bullets.append(AlienBullet(Point(), Animation(assets.alien_shots()[i]), i))

        self._spawn_tables.append(None)
        self._spawn_tables.append(itertools.cycle(game_settings.plunger_shot_spawn_table()))
        self._spawn_tables.append(itertools.cycle(game_settings.squiggly_shot_spawn_table()))

        for bullet in self._bullets:
            bullet._alive = False

    def tick(self, aliens):  # TODO use alien_grid
        i = self._to_shoot
        if not self._bullets[i]._alive:
            others = [self._bullets[j] for j in range(3) if i != j and self._bullets[j]._alive]
            min_ticks = min((bullet._ticks for bullet in others), default=None)
            # TODO score?
            if min_ticks is None or min_ticks > game_settings.alien_fire_speed(0):
                if i == 0:
                    playerx = self._game.player.position().x
                    x = (playerx - 24 - self._alien_grid._delta.x) // 16
                else:
                    x = next(self._spawn_tables[i]) - 1
                alien = next((alien for alien in aliens if alien.alive() and alien._coords.x == x), None)
                if alien:
                    self._bullets[i] = AlienBullet(alien.position() + Point(8, -8), Animation(assets.alien_shots()[i]), i)
                    self._game.spawn(self._bullets[i])
                    print(f"Spawning {i}, min_ticks {min_ticks}")
        self._to_shoot += 1
        self._to_shoot %= len(self._bullets)
