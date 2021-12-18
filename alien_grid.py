from point import Point
from animation import Animation
import assets
from dataclasses import dataclass
import game_object
from explosion import Explosion
from bullet import Bullet


@dataclass
class Alien(game_object.GameObject):
    alive: bool = True

    def __init__(self, game, coord):
        self.game = game
        self.position = Point(24 + coord.x * 16, 120 + coord.y * 16)
        alien_type = [0, 0, 1, 1, 2][coord.y]
        self._animation = Animation(assets.load_aliens()[alien_type])

    def sprite(self):
        return self._animation.sprite()

    def tick(self):
        pass

    def move(self, velocity):
        self.position += velocity
        self._animation.next()

    def on_collision(self, other):
        if isinstance(other, Bullet):
            self.game.explosions.append(
                Explosion(self.game, self.position, assets.alien_explosion(), 16)
            )
            self.alive = False


class AlienGrid:
    def __init__(self, game):
        self.game = game
        self._aliens = []
        self._delta = Point()
        self._velocity = Point(2, 0)
        for y in range(5):
            for x in range(11):
                self._aliens.append(Alien(self.game, Point(x, y)))
        self._alien_iter = iter(self._aliens)

    def tick(self):
        next_alien = next(
            (alien for alien in self._alien_iter if alien.alive), None
        )
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

    def aliens(self):
        return (alien for alien in self._aliens if alien.alive)
