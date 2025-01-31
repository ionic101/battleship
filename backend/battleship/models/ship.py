from battleship.models.player import Player
from battleship.models.coord import Coord


class Ship:
    def __init__(self, player: Player, coord: Coord, size: int, is_vertical: bool) -> None:
        self.player: Player = player
        self.coord: Coord = coord
        self.size: int = size
        self.is_vertical: bool = is_vertical
        self.lifes: int = size
