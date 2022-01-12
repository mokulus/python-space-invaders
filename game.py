from alien_system import AlienSystem
from player import Player
from point import Point
from bullet_system import BulletSystem
from shield_system import ShieldSystem
from gui_system import GuiSystem
from saucer_system import SaucerSystem
import itertools
from util import intersection, collision


class Game:
    def __init__(self):
        self.player = Player(self)
        self._score = 0
        try:
            with open("highscore.txt", "r") as file:
                self._highscore = int(file.read().strip())
                if self._highscore < 0:
                    raise ValueError
        except (FileNotFoundError, TypeError, ValueError):
            self._highscore = 0
        self._game_objects = [self.player]
        self._systems = []
        alien_system = AlienSystem(self)
        self._systems.append(alien_system)
        self._systems.append(BulletSystem(self, alien_system))
        self._systems.append(ShieldSystem(self))
        self._systems.append(GuiSystem(self))
        self._systems.append(SaucerSystem(self))

    def tick(self):
        for system in self._systems:
            system.tick()
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

    def add_score(self, score_change):
        self._score += score_change

    def score(self):
        return self._score

    def highscore(self):
        return self._highscore

    def exit(self):
        # FIXME save highscore every round
        with open("highscore.txt", "w") as file:
            file.write(f"{max(self._highscore, self._score)}\n")
