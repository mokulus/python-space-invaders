import itertools


class Animation:
    def __init__(self, sprites):
        self._sprites = itertools.cycle(iter(sprites))
        self.next()

    def sprite(self):
        return self._current_sprite

    def next(self):
        self._current_sprite = next(self._sprites)
        return self.sprite()
