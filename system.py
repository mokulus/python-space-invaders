from abc import ABC, abstractmethod


class System(ABC):
    @abstractmethod
    def tick(self):
        pass
