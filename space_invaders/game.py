"""
Provides :class:`Game`
"""
import itertools

from space_invaders import util
from space_invaders.alien_system import AlienSystem
from space_invaders.game_settings import CheatGameSettings, GameSettings
from space_invaders.gui_system import GuiSystem
from space_invaders.life_system import LifeSystem
from space_invaders.menu_system import MenuSystem
from space_invaders.player import Player
from space_invaders.shield_system import ShieldSystem


class Game:
    """
    Represents the Space Invaders game with the menu.

    To start the game create a `Game` instance and use either `load_menu` and
    call `play` on player's input or just `load_game`.

    Game should be `tick`ed every frame at 60 frames per second.

    When exiting `exit` should be called.
    """
    def __init__(self, cheats):
        """
        Initialize the `Game` object. Enable cheats if `cheats`.
        """
        self._score = 0
        self._round = 0
        self._ticks = 0
        self.player = None
        self._game_objects = []
        self._systems = []
        try:
            with open("highscore.txt", "r") as file:
                self._highscore = int(file.read().strip())
                if self._highscore < 0:
                    raise ValueError
        except (FileNotFoundError, TypeError, ValueError):
            self._highscore = 0
        self.settings = (
            GameSettings(self) if not cheats else CheatGameSettings(self)
        )

    def tick(self):
        """
        Update the game state. Should be called every frame at 60 frames per second.
        """
        for system in self._systems:
            system.tick()
        for game_object in self._game_objects:
            game_object.tick()
        self._game_objects = [
            game_object
            for game_object in self._game_objects
            if game_object.alive
        ]

        for first, second in itertools.combinations(self._game_objects, 2):
            if util.collision(first, second):
                first.on_collision(second)
                second.on_collision(first)
        self._ticks += 1

    def game_objects(self):
        """
        Return list of current game objects.
        """
        return self._game_objects

    def spawn(self, game_object):
        """
        Spawn a `game_object` `GameObject`.
        """
        self._game_objects.append(game_object)

    def add_system(self, system):
        """
        Add a `system` to current game `System`s.
        """
        self._systems.append(system)

    def add_score(self, score_change):
        """
        Adjust the game score by `score_change`.
        """
        self._score += score_change

    def score(self):
        """
        Return current score.
        """
        return self._score

    def highscore(self):
        """
        Return highscore.
        """
        return self._highscore

    def exit(self):
        """
        Call this function when exiting application.
        """
        self._save_highscore()

    def play(self):
        """
        If in menu, start the game. Otherwise do nothing.
        """
        if self.in_menu():
            self.player = Player(self)
            self.load_game()

    def _save_highscore(self):
        with open("highscore.txt", "w") as file:
            self._highscore = max(self._highscore, self._score)
            file.write(f"{self._highscore}\n")

    def reset(self):
        """
        Reset the game back to menu. Used when player loses all their lives or
        aliens get too close.
        """
        self._save_highscore()
        self._score = 0
        self._round = 0
        self.load_menu()

    def next_round(self):
        """
        Start the next round. Used when player kills all the aliens.
        """
        self._round += 1
        self.player.position().x = 0
        self.load_game()

    def load_game(self):
        """
        Load objects and systems for Space Invaders scene.
        """
        self._ticks = 0
        self._game_objects = []
        self._systems = []
        self._systems.append(AlienSystem(self))
        self._systems.append(ShieldSystem(self))
        self._systems.append(GuiSystem(self))
        self._systems.append(LifeSystem(self))

    def load_menu(self):
        """
        Load objects and systems for menu scene.
        """
        self.player = None
        self._ticks = 0
        self._game_objects = []
        self._systems = [MenuSystem(self)]
        self._systems.append(GuiSystem(self))

    def round(self):
        """
        Return current round number.
        """
        return self._round

    def ticks(self):
        """
        Return how many ticks were there since the start of the game.
        """
        return self._ticks

    def in_menu(self):
        """
        Check if the scene is menu.
        """
        return self.player is None
