from abc import abstractmethod

from space_invaders import game_object


class Bullet(game_object.GameObject):
    def __init__(self, game, position, animation, velocity):
        self._game = game
        self.alive = True
        self._position = position
        self._animation = animation
        self._velocity = velocity

    def position(self):
        return self._position

    def tick(self):
        self._position += self._velocity
        self._animation.next()

        if (
            self._position.y <= self._game.settings.game_area_y_bounds()[0]
            or self._position.y >= self._game.settings.game_area_y_bounds()[1]
        ):
            self.explode()

    def sprite(self):
        return self._animation.sprite()

    @abstractmethod
    def explode(self):
        self.alive = False
