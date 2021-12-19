import game_object
import game_settings


def inside(pos, size, max_pos):
    return size <= pos < max_pos - size


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

        if not inside(
            self._position.y,
            self.sprite().shape[1],
            game_settings.height(),
        ) or not inside(
            self._position.x,
            self.sprite().shape[0],
            game_settings.width(),
        ):
            self._alive = False

    def sprite(self):
        return self._animation.sprite()
