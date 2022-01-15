from abc import ABC, abstractmethod


class GameObject(ABC):
    @abstractmethod
    def alive(self):
        pass

    @abstractmethod
    def position(self):
        pass

    @abstractmethod
    def sprite(self):
        pass

    @abstractmethod
    def tick(self):
        pass

    @abstractmethod
    def on_collision(self, other):
        pass
