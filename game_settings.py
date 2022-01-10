def alient_initial_y(round_number):
    if round_number == 0:
        return 0x78
    lut = [0x60, 0x50, 0x48, 0x48, 0x48, 0x40, 0x40, 0x40]
    return lut[round_number % 10]


def width():
    return 224


def height():
    return 256


def alien_fire_speed(score):
    # FIXME
    return 0x30

def squiggly_shot_spawn_table():
    return [0x0B, 0x01, 0x06, 0x03, 0x01, 0x01, 0x0B, 0x09, 0x02]
