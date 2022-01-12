from point import Point
import numpy as np


def intersection(a_pos, a_sprite, b_pos, b_sprite):
    minx = max(a_pos[0], b_pos[0])
    maxx = min(
        a_pos[0] + a_sprite.shape[0],
        b_pos[0] + b_sprite.shape[0],
    )
    miny = max(a_pos[1], b_pos[1])
    maxy = min(
        a_pos[1] + a_sprite.shape[1],
        b_pos[1] + b_sprite.shape[1],
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
    intersection_rect = intersection(a.position(), a.sprite(), b.position(), b.sprite())
    if intersection_rect is None:
        return False
    return (sprite_view(a, intersection_rect) * sprite_view(b, intersection_rect)).any()