import game_object


class Explosion(game_object.GameObject):
    def __init__(self, game, position, sprite, frames):
        self.game = game
        self.position = position
        self._sprite = sprite
        self.frames = frames

    def tick(self):
        self.frames -= 1

    def sprite(self):
        return self._sprite

    def on_collision(self, other):
        pass
