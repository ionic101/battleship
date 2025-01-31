from pydantic import BaseModel, field_validator
from battleship.models.colors import Colors
from uuid import UUID
from battleship.utils.config import config


class CoordScheme(BaseModel):
    x: int
    y: int

    @field_validator('x')
    def x_validate(cls, x: int) -> int:
        if x >= 0 and x < config.BOARD_WIDTH:
            return x
        raise ValueError(f'Field "x" must be must be in the range from 0 to {config.BOARD_WIDTH}')
    
    @field_validator('y')
    def y_validate(cls, y: int) -> int:
        if y >= 0 and y < config.BOARD_HEIGHT:
            return y
        raise ValueError(f'Field "y" must be must be in the range from 0 to {config.BOARD_HEIGHT}')
