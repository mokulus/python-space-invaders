import numpy as np
from functools import cache


def _load_chunk(lines):
    chunk_lines = []
    for line in lines:
        if line:
            chunk_lines.append(line)
        else:
            break
    chunk = " ".join(chunk_lines)
    data = [int(value, 16) for value in chunk.split()]
    data = np.array(data, dtype=np.uint8)
    data = np.unpackbits(data)
    return data

def _data_lines(file_name):
    with open(file_name, "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        return lines

def _load_single_sprite(file_name, shape, flip=False):
    data = _load_chunk(_data_lines(file_name))
    if flip:
        data = np.flip(data)
    data = np.reshape(data, shape)
    return data

@cache
def aliens():
    aliens = []
    lines = _data_lines("./assets/aliens.txt")
    for pair in zip(lines[::2], lines[1::2]):
        data = _load_chunk(pair)
        data = np.reshape(data, (2, 16, 8))
        aliens.append(data)
    return aliens

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
