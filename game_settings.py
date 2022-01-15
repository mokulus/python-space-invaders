import bisect


class GameSettings():
    def __init__(self, game):
        self._game = game

    def alien_initial_y(self):
        lut = [0x78, 0x60, 0x50, 0x48, 0x48, 0x48, 0x40]
        if self._game.round() >= len(lut):
            return lut[-1]
        else:
            return lut[self._game.round()]

    def width(self):
        return 224

    def height(self):
        return 256

    def alien_fire_period(self):
        periods = [0x30, 0x10, 0x0B, 0x08, 0x07]
        scores = [200, 1000, 2000, 3000]
        return 3 * periods[bisect.bisect_left(scores, self._game.score())]

    def shot_spawn_table(self):
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
        return self.shot_spawn_table()[6:21]

    def plunger_shot_spawn_table(self):
        return self.shot_spawn_table()[0:16]

    def saucer_score(self):
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

    def game_area_y_bounds(self):
        return (8, 212)

    def saucer_period(self):
        return 600
