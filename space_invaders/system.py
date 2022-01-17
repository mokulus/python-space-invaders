"""
Provides :class:`System`
"""
from abc import ABC


class System(ABC):
    """
    Abstract class representing a system that can be updated every frame.
    """

    def tick(self):
        """
        Update the system.
        """
