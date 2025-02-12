from uuid import UUID

from pydantic import BaseModel


class RejoinGameScheme(BaseModel):
    player_uuid: UUID
