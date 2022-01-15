from space_invaders import game_object


class Explosion(game_object.GameObject):
    def __init__(self, position, sprite, frames):
        self.alive = True
        self._position = position
        self._sprite = sprite
        self._frames = frames

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def tick(self):
        self._frames -= 1
        if self._frames <= 0:
            self.alive = False

    def on_collision(self, other):
        pass
