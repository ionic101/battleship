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
        'action': 'new_shot',
        'shot': {
            'type': shot.type.value,
            'coord': {
                'x': shot.coord.x,
                'y': shot.coord.y,
            }
        }
    }
    if shot.type != ShotType.MISS and shot.ship is not None:
        response['shot']['color'] = shot.ship.player.color.value
    return response


async def action_shot(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    shot_data: ShotScheme | None = await WebSocketUtils.get_field(ShotScheme, websocket, data)
    if shot_data is None:
        return

    who_move: Player = game.get_who_move()
    if shot_data.player_uuid != who_move.uuid:
        await WebSocketUtils.send_error(websocket, 'shot', f'Player with uuid {shot_data.player_uuid} can\'t move now')
        return

    coord_model: Coord = Coord(**shot_data.shot_coord.model_dump())
    if coord_model in game.board.shots or coord_model in game.board.ships_coords and game.board.ships_coords[coord_model].player.uuid == shot_data.player_uuid:
        await WebSocketUtils.send_error(websocket, 'shot', f'Cell is not available for shot')
        return
    
    shot_info: ShotInfo = game.board.shot(coord_model)
    if shot_info.type == ShotType.MISS:
        await game.player_move()
    await websocket.send_json({'action': 'shot', 'status': 'ok'})
    await game.broadcast(get_response_shot_data(shot_info))
    
    if shot_info.type == ShotType.DESTROY and shot_info.ship is not None:
        shots: list[ShotInfo] = []
        start_coord = shot_info.ship.coord + Coord(-1, -1)
        if shot_info.ship.is_vertical:
            shots.append(game.board.shot(start_coord + Coord(1, 0)))
            shots.append(game.board.shot(start_coord + Coord(1, shot_info.ship.size + 1)))
        else:
            shots.append(game.board.shot(start_coord + Coord(0, 1)))
            shots.append(game.board.shot(start_coord + Coord(shot_info.ship.size + 1, 1)))
        for d in range(0, shot_info.ship.size + 2):
            if shot_info.ship.is_vertical:
                shots.append(game.board.shot(start_coord + Coord(0, d)))
                shots.append(game.board.shot(start_coord + Coord(2, d)))
            else:
                shots.append(game.board.shot(start_coord + Coord(d, 0)))
                shots.append(game.board.shot(start_coord + Coord(d, 2)))
        for shot in shots:
            await game.broadcast(get_response_shot_data(shot))
