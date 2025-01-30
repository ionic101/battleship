from fastapi import APIRouter
from typing import List
from battleship.routers.game import game_router
from battleship.routers.websockets import ws_router


routers: List[APIRouter] = [
    game_router,
    ws_router
]

__all__ = [
    'routers'
]
