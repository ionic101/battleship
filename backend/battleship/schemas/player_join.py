from pydantic import BaseModel, field_validator
from battleship.models.colors import Colors


class PlayerJoin(BaseModel):
    username: str
    color: Colors
