from alien_grid import AlienGrid
from player import Player
from point import Point
import itertools


class Game:
    def __init__(self):
        self.player = Player(self)
        self._game_objects = [self.player]
        self._alien_grid = AlienGrid(self)

    def tick(self):
        # TODO order?
        self._alien_grid.tick()
        for game_object in self._game_objects:
            game_object.tick()
        self._game_objects = [
            game_object
            for game_object in self._game_objects
            if game_object.alive()
        ]

    def collision(self):
        for a, b in itertools.combinations(self._game_objects, 2):
            if collision(a, b):
                a.on_collision(b)
                b.on_collision(a)

    def game_objects(self):
        return self._game_objects

    def spawn(self, game_object):
        self._game_objects.append(game_object)


def intersection(a, b):
    minx = max(a.position()[0], b.position()[0])
    maxx = min(
        a.position()[0] + a.sprite().shape[0],
        b.position()[0] + b.sprite().shape[0],
    )
    miny = max(a.position()[1], b.position()[1])
    maxy = min(
        a.position()[1] + a.sprite().shape[1],
        b.position()[1] + b.sprite().shape[1],
    )
    if minx <= maxx and miny <= maxy:
        return (Point(minx, maxx), Point(miny, maxy))
    else:
        return None


def collision(a, b):
    intersection_rect = intersection(a, b)
    if intersection_rect is None:
        return False
    (minx, maxx), (miny, maxy) = intersection_rect

    def sprite_view(obj):
        return obj.sprite()[
            minx - obj.position()[0]: maxx - obj.position()[0],
            miny - obj.position()[1]: maxy - obj.position()[1],
        ]

    return (sprite_view(a) * sprite_view(b)).any()
