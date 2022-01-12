from alien_system import AlienSystem
from player import Player
from point import Point
from bullet_system import BulletSystem
from shield_system import ShieldSystem
import itertools
from util import intersection, collision


class Game:
    def __init__(self):
        self.player = Player(self)
        self._game_objects = [self.player]
        self._alien_system = AlienSystem(self)
        self._bullet_system = BulletSystem(self, self._alien_system)
        self._shield_system = ShieldSystem(self)

    def tick(self):
        # TODO order?
        self._alien_system.tick()
        self._bullet_system.tick()
        for game_object in self._game_objects:
            game_object.tick()
        self._game_objects = [
            game_object
            for game_object in self._game_objects
            if game_object.alive()
        ]

    def collision(self):
        for a, b in itertools.combinations(self._game_objects, 2):
            if collision(a, b):
                a.on_collision(b)
                b.on_collision(a)

    def game_objects(self):
        return self._game_objects

    def spawn(self, game_object):
        self._game_objects.append(game_object)
