import numpy as np


def load_chunk(lines):
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


def load_aliens():
    aliens = []
    with open("./assets/aliens.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        for pair in zip(lines[::2], lines[1::2]):
            data = load_chunk(pair)
            data = np.reshape(data, (2, 16, 8))
            aliens.append(data)
    return aliens


def load_player():
    with open("./assets/player.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        data = load_chunk(lines)
        data = np.reshape(data, (16, 8))
        return data


def load_player_shot():
    with open("./assets/player_shot.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        data = load_chunk(lines)
        data = np.flip(data)
        data = np.reshape(data, (1, 8))
        return data


def player_shot_explosion():
    with open("./assets/player_shot_explosion.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        data = load_chunk(lines)
        data = np.reshape(data, (8, 8))
        return data


def alien_explosion():
    with open("./assets/alien_explosion.txt", "r") as file:
        lines = [line.strip() for line in file if line.strip()]
        data = load_chunk(lines)
        data = np.reshape(data, (16, 8))
        return data
