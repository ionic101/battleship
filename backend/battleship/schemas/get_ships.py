from uuid import UUID

from pydantic import BaseModel


class GetShipsScheme(BaseModel):
    player_uuid: UUID
