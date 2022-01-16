"""
Provides :class:`GameObject`
"""
from abc import ABC, abstractmethod


class GameObject(ABC):
    """
    Represents a game object that can be destroyed, has position, sprite,
    color, and responds to collision.

    Attributes:
        alive    bool representing if object is alive. Dead object shouldn't be
                 update by the `Game`
        color    tuple of 3 ints in range 0 to 255 representing the color the
                 object is drawn with
    """
    def __init__(self):
        self.alive = True
        self.color = (255, 255, 255)

    @abstractmethod
    def position(self):
        """
        Return point representing the positon of the object.
        """

    @abstractmethod
    def sprite(self):
        """
        Return sprite representing the object. Used for drawing and collision
        detection.
        """

    def tick(self):
        """
        Update the game object.
        """

    def on_collision(self, other):
        """
        Callback used when object collides with `other`. Ignore or respond to
        it based on the type of `other`.
        """
