from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.shot_type import ShotType


async def action_get_shots(websocket: WebSocket, game: Game, **kwargs) -> None:
    response: list[dict[str, Any]] = []
    for shot_coord in game.board.shots:
        shot_data: dict[str, Any] = {
            'type': game.board.shots[shot_coord],
            'coord': {
                'x': shot_coord.x,
                'y': shot_coord.y
            }
        }
        if game.board.shots[shot_coord] != ShotType.MISS:
            shot_data['color'] = game.board.ships_coords[shot_coord].player.color.value
        response.append(shot_data)
    await websocket.send_json(response)
