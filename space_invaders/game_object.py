from abc import ABC, abstractmethod


class GameObject(ABC):
    def __init__(self):
        self.alive = True

    @abstractmethod
    def position(self):
        pass

    @abstractmethod
    def sprite(self):
        pass

    def tick(self):
        pass

    def on_collision(self, other):
        pass
