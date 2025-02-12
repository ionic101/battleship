from random import randint
from dataclasses import dataclass

@dataclass
class Coord:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    @staticmethod
    def get_random(start: 'Coord', end: 'Coord') -> 'Coord':
        return Coord(randint(start.x, end.x), randint(start.y, end.y))
    
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Coord) and self.x == other.x and self.y == other.y
