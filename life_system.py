import system
from text_object import VariableTextObject
from static_sprite import StaticSprite
from point import Point
import assets


class LifeSystem(system.System):
    def __init__(self, game):
        self._game = game
        self._number_object = VariableTextObject(
            self._game, Point(8, 0), lambda g: str(g.player.lives())
        )
        self._game.spawn(self._number_object)
        self._player_objects = []
        self._remake_player_sprites()

    def tick(self):
        if self._game.player.lives() - 1 != len(self._player_objects):
            self._remake_player_sprites()

    def _remake_player_sprites(self):
        for obj in self._player_objects:
            obj._alive = False
        self._player_objects = []
        for i in range(self._game.player.lives() - 1):
            sprite = assets.player()
            self._player_objects.append(
                StaticSprite(Point(3 * 8 + sprite.shape[0] * i, 0), sprite)
            )
            self._game.spawn(self._player_objects[-1])
