from functools import cache

import numpy as np


def _load_chunk(lines):
    chunk = " ".join(lines)
    data = [int(value, 16) for value in chunk.split()]
    data = np.array(data, dtype=np.uint8)
    data = np.unpackbits(data)
    return data


def _data_lines(file_name):
    with open(file_name, "r") as file:
        lines = [line.split("#")[0].strip() for line in file]
        lines = [line for line in lines if line]
        return lines


def _lines_to_sprites(lines, shape):
    sprites = []
    for line in lines:
        data = _load_chunk([line])
        data = np.reshape(data, shape)
        sprites.append(data)
    return sprites


def _load_single_sprite(file_name, shape, flip=False):
    data = _load_chunk(_data_lines(file_name))
    if flip:
        data = np.flip(data)
    data = np.reshape(data, shape)
    return data


@cache
def aliens():
    pairs = []
    lines = _data_lines("./assets/aliens.txt")
    for pair in zip(lines[::2], lines[1::2]):
        data = _load_chunk(pair)
        data = np.reshape(data, (2, 16, 8))
        pairs.append(data)
    return pairs


@cache
def player():
    return _load_single_sprite("./assets/player.txt", (16, 8))


@cache
def player_shot():
    return _load_single_sprite("./assets/player_shot.txt", (1, 8), flip=True)


@cache
def player_shot_explosion():
    return _load_single_sprite("./assets/player_shot_explosion.txt", (8, 8))


@cache
def alien_explosion():
    return _load_single_sprite("./assets/alien_explosion.txt", (16, 8))


@cache
def alien_shots():
    shots = []
    lines = _data_lines("./assets/alien_shots.txt")
    size = 4
    for offset in range(3):
        data = _load_chunk(lines[offset * size : (offset + 1) * size])
        data = np.reshape(data, (4, 3, 8))
        shots.append(data)
    return shots


@cache
def alien_shot_explosion():
    return _load_single_sprite("./assets/alien_shot_explosion.txt", (6, 8))


@cache
def shield():
    return _load_single_sprite("./assets/shield.txt", (22, 16))


@cache
def font():
    lines = _data_lines("./assets/font.txt")
    return _lines_to_sprites(lines, (8, 8))


def font_characters():
    return "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789<> =?-"


@cache
def saucer():
    return _load_single_sprite("./assets/saucer.txt", (24, 8))


@cache
def saucer_explosion():
    return _load_single_sprite("./assets/saucer_explosion.txt", (24, 8))


@cache
def player_explosion():
    lines = _data_lines("./assets/player_explosion.txt")
    return _lines_to_sprites(lines, (16, 8))


def empty_sprite():
    return np.zeros((0, 0), dtype=np.uint8)
