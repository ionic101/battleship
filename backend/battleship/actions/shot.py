from typing import Any, TypeVar

from fastapi import WebSocket
from pydantic import ValidationError

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.models.coord import Coord
from battleship.schemas.shot import ShotScheme
from battleship.models.shot_info import ShotInfo
from battleship.models.shot_type import ShotType



T = TypeVar('T')


async def get_field(field_scheme: type[T], websocket: WebSocket, data: dict[str, Any]) -> T | None:
    try:
        return field_scheme(**data)
    except ValidationError as e:
        await WebSocketUtils.send_error(websocket, data['action'], e.errors()[0]['msg'])


def get_response_shot_data(shot: ShotInfo) -> dict[str, Any]:
    response: dict[str, Any] = {}
    match shot.type:
        case ShotType.MISS:
            response['type'] = 'miss'
            response['coord'] = {
                'x': shot.coord.x,
                'y': shot.coord.y,
            }
        case ShotType.HIT:
            response['type'] = 'hit'
            response['coord'] = {
                'x': shot.coord.x,
                'y': shot.coord.y,
            }
            if shot.ship is not None:
                response['color'] = shot.ship.player.color.value
        case ShotType.DESTROY:
            response['type'] = 'destroy'
            response['coord'] = {
                'x': shot.coord.x,
                'y': shot.coord.y,
            }
            if shot.ship is not None:
                response['color'] = shot.ship.player.color.value
    return response


# TODO: refactor
async def action_shot(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    shot_data: ShotScheme | None = await get_field(ShotScheme, websocket, data)
    if shot_data is None:
        return

    who_move: Player = game.get_who_move()
    if shot_data.player_uuid != who_move.uuid:
        await WebSocketUtils.send_error(websocket, 'shot', f'Player with uuid {shot_data.player_uuid} can\'t move now')

    if Coord(**shot_data.shot_coord.model_dump()) in game.board.shots:
        await WebSocketUtils.send_error(websocket, 'shot', f'Cell is not available for shot')
    
    shot_info: ShotInfo = game.board.shot(Coord(**shot_data.shot_coord.model_dump()))
    if shot_info.type == ShotType.MISS:
        await game.player_move()
    await websocket.send_json({'action': 'shot', 'status': 'ok'})
    await game.broadcast(get_response_shot_data(shot_info))
