from pydantic import BaseModel

from battleship.models.colors import Colors


class PlayerJoin(BaseModel):
    username: str
    color: Colors
