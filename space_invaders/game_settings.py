"""
Provides :class:`GameSettings` and :class:`CheatGameSettings`
"""
import bisect


class GameSettings:
    """
    Game settings for playing without cheats.
    """
    def __init__(self, game):
        self._game = game

    def alien_initial_y(self):
        """
        Return initial y coordinate of the bottom-left alien based.
        """
        lut = [0x78, 0x60, 0x50, 0x48, 0x48, 0x48, 0x40]
        if self._game.round() >= len(lut):
            return lut[-1]
        return lut[self._game.round()]

    @staticmethod
    def width():
        """
        Return the game screen width.
        """
        return 224

    @staticmethod
    def height():
        """
        Return the game screen height.
        """
        return 256

    def alien_fire_period(self):
        """
        Return the current delay between shots.
        """
        periods = [0x30, 0x10, 0x0B, 0x08, 0x07]
        scores = [200, 1000, 2000, 3000]
        return 3 * periods[bisect.bisect_left(scores, self._game.score())]

    @staticmethod
    def shot_spawn_table():
        """
        Return the table of one-based columns in which to spawn aliens.
        """
        return [
            0x01,
            0x07,
            0x01,
            0x01,
            0x01,
            0x04,
            0x0B,
            0x01,
            0x06,
            0x03,
            0x01,
            0x01,
            0x0B,
            0x09,
            0x02,
            0x08,
            0x02,
            0x0B,
            0x04,
            0x07,
            0x0A,
        ]

    def squiggly_shot_spawn_table(self):
        """
        Return the one-based columns in which to spawn "squiggly" shots.
        """
        return self.shot_spawn_table()[6:21]

    def plunger_shot_spawn_table(self):
        """
        Return the one-based columns in which to spawn "plunger" shots.
        """
        return self.shot_spawn_table()[0:16]

    def saucer_score(self):
        """
        Return the score that destroying saucer would give.
        """
        scores = [
            100,
            50,
            50,
            100,
            150,
            100,
            100,
            50,
            300,
            100,
            100,
            100,
            50,
            150,
            100,
            50,
        ]
        return scores[self._game.player.shots_fired() % len(scores)]

    @staticmethod
    def game_area_y_bounds():
        """
        Return a `tuple` of 2 `int`s with minimum and maximum y coordinates for
        bullets.
        """
        return (8, 212)

    @staticmethod
    def saucer_period():
        """
        Return the delay between saucer spawns.
        """
        return 600

    @staticmethod
    def infinite_bullets():
        """
        Check if player should have infinite bullets.
        """
        return False

    @staticmethod
    def invincibility():
        """
        Check if invincibility should be enabled.
        """
        return False


class CheatGameSettings(GameSettings):
    """
    Game settings for playing with cheats.
    """
    @staticmethod
    def saucer_period():
        return 60

    @staticmethod
    def infinite_bullets():
        return True

    @staticmethod
    def invincibility():
        return True
