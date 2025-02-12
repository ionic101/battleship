from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.models.coord import Coord
from battleship.schemas.shot import ShotScheme
from battleship.models.shot_info import ShotInfo
from battleship.models.shot_type import ShotType


def get_response_shot_data(shot: ShotInfo) -> dict[str, Any]:
    response: dict[str, Any] = {
        'type': shot.type.value,
        'coord': {
            'x': shot.coord.x,
            'y': shot.coord.y,
        }
    }
    if shot.type != ShotType.MISS and shot.ship is not None:
        response['color'] = shot.ship.player.color.value
    return response


async def action_shot(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    shot_data: ShotScheme | None = await WebSocketUtils.get_field(ShotScheme, websocket, data)
    if shot_data is None:
        return

    who_move: Player = game.get_who_move()
    if shot_data.player_uuid != who_move.uuid:
        await WebSocketUtils.send_error(websocket, 'shot', f'Player with uuid {shot_data.player_uuid} can\'t move now')

    coord_model: Coord = Coord(**shot_data.shot_coord.model_dump())
    if coord_model in game.board.shots:
        await WebSocketUtils.send_error(websocket, 'shot', f'Cell is not available for shot')
    
    shot_info: ShotInfo = game.board.shot(coord_model)
    if shot_info.type == ShotType.MISS:
        await game.player_move()
    await websocket.send_json({'action': 'shot', 'status': 'ok'})
    await game.broadcast(get_response_shot_data(shot_info))
