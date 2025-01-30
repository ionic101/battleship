from pydantic import BaseModel

from battleship.schemas.player_join import PlayerJoin


schemas: list[type[BaseModel]] = [
    PlayerJoin
]

__all__ = [
    'schemas'
]
