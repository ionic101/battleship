from battleship.models.shot_type import ShotType
from battleship.models.ship import Ship


class ShotInfo:
    def __init__(self, shot_type: ShotType, ship: Ship | None) -> None:
        self.type: ShotType = shot_type
        self.ship: Ship | None = ship
