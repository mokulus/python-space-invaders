import bisect


def alien_initial_y(round_number):
    lut = [0x78, 0x60, 0x50, 0x48, 0x48, 0x48, 0x40]
    if round_number >= len(lut):
        return lut[-1]
    else:
        return lut[round_number]


def width():
    return 224


def height():
    return 256


def alien_fire_period(score):
    periods = [0x30, 0x10, 0x0B, 0x08, 0x07]
    scores = [200, 1000, 2000, 3000]
    return periods[bisect.bisect_left(scores, score)]


def shot_spawn_table():
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


def squiggly_shot_spawn_table():
    return shot_spawn_table()[6:21]


def plunger_shot_spawn_table():
    return shot_spawn_table()[0:16]


def saucer_score(shots_fired):
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
    return scores[shots_fired % len(scores)]
