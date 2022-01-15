import numpy as np

import assets
from point import Point


def intersection(a_pos, a_sprite, b_pos, b_sprite):
    minx = max(a_pos.x, b_pos.x)
    maxx = min(
        a_pos.x + a_sprite.shape[0],
        b_pos.x + b_sprite.shape[0],
    )
    miny = max(a_pos.y, b_pos.y)
    maxy = min(
        a_pos.y + a_sprite.shape[1],
        b_pos.y + b_sprite.shape[1],
    )
    if minx <= maxx and miny <= maxy:
        return (Point(minx, maxx), Point(miny, maxy))
    else:
        return None


def sprite_view(obj, intersection_rect):
    (minx, maxx), (miny, maxy) = intersection_rect
    sprite = np.fliplr(obj.sprite())
    return sprite[
        minx - obj.position()[0]: maxx - obj.position()[0],
        miny - obj.position()[1]: maxy - obj.position()[1],
    ]


def collision(a, b):
    intersection_rect = intersection(
        a.position(), a.sprite(), b.position(), b.sprite()
    )
    if intersection_rect is None:
        return False
    return (
        sprite_view(a, intersection_rect) * sprite_view(b, intersection_rect)
    ).any()


def text_to_sprite(str):
    sprite = np.zeros((8 * len(str), 8), dtype=np.uint8)
    font = assets.font()
    font_characters = assets.font_characters()
    for i in range(len(str)):
        sprite[8 * i: 8 * (i + 1), :] = font[font_characters.index(str[i])]
    return sprite


def padding(width, text=None):
    if text is None:
        text = ""
    return (width - 8 * len(text)) // 2 // 8 * 8
