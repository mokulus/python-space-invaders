from point import Point
from animation import Animation
import assets
import game_settings
from dataclasses import dataclass
import game_object
from explosion import Explosion
import player_bullet
from alien_bullet import AlienBullet
import system
from bullet_system import BulletSystem
from saucer_system import SaucerSystem


class Alien(game_object.GameObject):
    def __init__(self, game, coords, alien_system):
        self._alive = True
        self._coords = coords
        self._alien_system = alien_system
        self._position = Point(
            24 + coords.x * 16,
            game_settings.alien_initial_y(game.round()) + coords.y * 16,
        )
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
        if isinstance(other, player_bullet.PlayerBullet):
            self._game.spawn(
                Explosion(self._position, assets.alien_explosion(), 16)
            )
            self._alive = False
            self._game.add_score([10, 10, 20, 20, 30][self._coords.y])

    def move(self, velocity):
        self._position += velocity
        self._animation.next()

    def coords(self):
        return self._coords

    @staticmethod
    def _get_sprite(y):
        alien_type = [0, 0, 1, 1, 2][y]
        return Animation(assets.aliens()[alien_type])


class AlienSystem(system.System):
    def __init__(self, game):
        self._game = game
        self._aliens = []
        self._delta = Point()
        self._velocity = Point(2, 0)
        for y in range(5):
            for x in range(11):
                alien = Alien(self._game, Point(x, y), self)
                self._aliens.append(alien)
        self._alien_iter = iter(self._aliens)
        self._initialized = False
        self._init_ticks = 0

    def tick(self):
        if not self._initialized:
            self._init_animation()
            return
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
        if not any(alien.alive() for alien in self._aliens):
            self._game.next_round()

    def _init_animation(self):
        self._init_ticks += 1
        if self._init_ticks % 2 != 0:
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

    def alien_count(self):
        return sum(alien.alive for alien in self._aliens)

    def aliens(self):
        return self._aliens

    def delta(self):
        return self._delta

    def initialized(self):
        return self._initialized
