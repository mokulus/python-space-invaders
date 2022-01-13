import game_object


class StaticSprite(game_object.GameObject):
    def __init__(self, position, sprite):
        self._position = position
        self._sprite = sprite

    def alive(self):
        return True

    def position(self):
        return self._position

    def sprite(self):
        return self._sprite

    def tick(self):
        pass

    def on_collision(self, other):
        pass
