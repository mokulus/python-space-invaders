import numpy as np

from space_invaders import assets
from space_invaders.point import Point


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
    return None


def sprite_view(obj, intersection_rect):
    (minx, maxx), (miny, maxy) = intersection_rect
    sprite = np.fliplr(obj.sprite())
    return sprite[
        minx - obj.position()[0] : maxx - obj.position()[0],
        miny - obj.position()[1] : maxy - obj.position()[1],
    ]


def collision(first, second):
    intersection_rect = intersection(
        first.position(), first.sprite(), second.position(), second.sprite()
    )
    if intersection_rect is None:
        return False
    return (
        sprite_view(first, intersection_rect)
        * sprite_view(second, intersection_rect)
    ).any()


def text_to_sprite(text):
    sprite = np.zeros((8 * len(text), 8), dtype=np.uint8)
    font = assets.font()
    font_characters = assets.font_characters()
    for i, char in enumerate(text):
        sprite[8 * i : 8 * (i + 1), :] = font[font_characters.index(char)]
    return sprite


def padding(width, text=None):
    if text is None:
        text = ""
    return (width - 8 * len(text)) // 2 // 8 * 8
