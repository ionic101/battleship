from random import randint


class Coord:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def __add__(self, other):
        if isinstance(other, Coord):
            return Coord(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    @staticmethod
    def get_random(start: 'Coord', end: 'Coord') -> 'Coord':
        return Coord(randint(start.x, end.x), randint(start.y, end.y))
