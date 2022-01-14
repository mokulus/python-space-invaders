from abc import abstractmethod
import game_object
import game_settings


class Bullet(game_object.GameObject):
    def __init__(self, position, animation, velocity):
        self._alive = True
        self._position = position
        self._animation = animation
        self._velocity = velocity

    def alive(self):
        return self._alive

    def position(self):
        return self._position

    def tick(self):
        self._position += self._velocity
        self._animation.next()

        if (
            self._position.y <= game_settings.game_area_y_bounds()[0]
            or self._position.y >= game_settings.game_area_y_bounds()[1]
        ):
            self.explode()

    def sprite(self):
        return self._animation.sprite()

    @abstractmethod
    def explode(self):
        self._alive = False
