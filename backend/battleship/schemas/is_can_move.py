from pydantic import BaseModel, field_validator
from battleship.models.colors import Colors
from uuid import UUID
from battleship.schemas.coord import CoordScheme


class IsCanMoveScheme(BaseModel):
    player_uuid: UUID
