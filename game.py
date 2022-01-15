import itertools

import util
from alien_system import AlienSystem
from game_settings import CheatGameSettings, GameSettings
from gui_system import GuiSystem
from life_system import LifeSystem
from menu import MenuSystem
from player import Player
from shield_system import ShieldSystem


class Game:
    def __init__(self, cheats):
        self._score = 0
        self._round = 0
        self._ticks = 0
        try:
            with open("highscore.txt", "r") as file:
                self._highscore = int(file.read().strip())
                if self._highscore < 0:
                    raise ValueError
        except (FileNotFoundError, TypeError, ValueError):
            self._highscore = 0
        self.settings = GameSettings(
            self) if not cheats else CheatGameSettings(self)
        self._load_menu()

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

        for a, b in itertools.combinations(self._game_objects, 2):
            if util.collision(a, b):
                a.on_collision(b)
                b.on_collision(a)
        self._ticks += 1

    def game_objects(self):
        return self._game_objects

    def spawn(self, game_object):
        self._game_objects.append(game_object)

    def add_system(self, system):
        self._systems.append(system)

    def add_score(self, score_change):
        self._score += score_change

    def score(self):
        return self._score

    def highscore(self):
        return self._highscore

    def exit(self):
        self._save_highscore()

    def play(self):
        if self.player is None:
            self.player = Player(self)
            self._load_game()

    def _save_highscore(self):
        with open("highscore.txt", "w") as file:
            self._highscore = max(self._highscore, self._score)
            file.write(f"{self._highscore}\n")

    def reset(self):
        self._save_highscore()
        self._score = 0
        self._round = 0
        self._load_menu()

    def next_round(self):
        self._round += 1
        self.player._position.x = 0
        self._load_game()

    def _load_game(self):
        self._game_objects = []
        self._systems = []
        alien_system = AlienSystem(self)
        self._systems.append(alien_system)
        self._systems.append(ShieldSystem(self))
        self._systems.append(GuiSystem(self))
        self._systems.append(LifeSystem(self))

    def _load_menu(self):
        self.player = None
        self._game_objects = []
        self._systems = [MenuSystem(self)]
        self._systems.append(GuiSystem(self))

    def round(self):
        return self._round

    def ticks(self):
        return self._ticks
