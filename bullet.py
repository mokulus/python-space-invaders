import game_object


class Bullet(game_object.GameObject):
    def __init__(self, game, position, animation, velocity):
        self.game = game
        self.position = position
        self._animation = animation
        self._velocity = velocity

    def tick(self):
        self.position += self._velocity
        self._animation.next()

    def sprite(self):
        return self._animation.sprite()
