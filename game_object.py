from dataclasses import dataclass
from abc import ABC, abstractmethod
from point import Point


@dataclass
class GameObject(ABC):
    position: Point

    @abstractmethod
    def sprite(self):
        pass

    @abstractmethod
    def tick(self, game):
        pass

    @abstractmethod
    def on_collision(self, other, game):
        pass
