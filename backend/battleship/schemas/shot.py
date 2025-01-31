from pydantic import BaseModel, field_validator
from battleship.models.colors import Colors
from uuid import UUID
from battleship.schemas.coord import CoordScheme


class ShotScheme(BaseModel):
    player_uuid: UUID
    shot_coord: CoordScheme
