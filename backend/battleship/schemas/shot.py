from uuid import UUID

from pydantic import BaseModel

from battleship.schemas.coord import CoordScheme


class ShotScheme(BaseModel):
    player_uuid: UUID
    shot_coord: CoordScheme
