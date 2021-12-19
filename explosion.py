import game_object


class Explosion(game_object.GameObject):
    def __init__(self, position, sprite, frames):
        self._position = position
        self._sprite = sprite
        self._frames = frames

    def alive(self):
        return self._frames > 0

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def tick(self):
        self._frames -= 1

    def on_collision(self, other):
        pass
