from dataclasses import dataclass


@dataclass
class Point:
    x: int = 0
    y: int = 0

    def __getitem__(self, key):
        Point._validate_key(key)
        if key == 0:
            return self.x
        return self.y

    def __setitem__(self, key, value):
        Point._validate_key(key)
        if key == 0:
            self.x = value
        else:
            self.y = value

    @staticmethod
    def _validate_key(key):
        if key not in (0, 1):
            raise IndexError(f"index {key} outside of range")

    def __len__(self):
        return 2

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1])

    def __sub__(self, other):
        return Point(self.x - other[0], self.y - other[1])
