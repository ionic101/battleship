from battleship.models.shot_type import ShotType
from battleship.models.ship import Ship
from battleship.models.coord import Coord


class ShotInfo:
    def __init__(self, shot_type: ShotType, coord: Coord, ship: Ship | None = None) -> None:
        self.type: ShotType = shot_type
        self.ship: Ship | None = ship
        self.coord: Coord = coord