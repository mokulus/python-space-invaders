from point import Point
from animation import Animation
import assets
from dataclasses import dataclass
import game_object
from explosion import Explosion
from bullet import Bullet


@dataclass
class Alien(game_object.GameObject):
    def __init__(self, game, coords):
        self._alive = True
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
        return Animation(assets.load_aliens()[alien_type])


class AlienGrid:
    def __init__(self, game):
        self._aliens = []
        self._delta = Point()
        self._velocity = Point(2, 0)
        for y in range(5):
            for x in range(11):
                alien = Alien(game, Point(x, y))
                self._aliens.append(alien)
                game.spawn(alien)
        self._alien_iter = iter(self._aliens)

    def tick(self):
        self._alien_iter = (
            alien for alien in self._alien_iter if alien.alive
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
