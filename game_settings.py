def alient_initial_y(round_number):
    if round_number == 0:
        return 0x78
    lut = [0x60, 0x50, 0x48, 0x48, 0x48, 0x40, 0x40, 0x40]
    return lut[round_number % 10]


def width():
    return 224


def height():
    return 256
