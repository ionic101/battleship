from typing import Any

from fastapi import WebSocket
from uuid import UUID

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.models.game_status import GameStatus
from battleship.models.ship import Ship


# TODO: refactor
async def action_get_ships(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    if game.status != GameStatus.IN_GAME:
        await WebSocketUtils.send_error(websocket, 'get_ships', 'Game not started')
    player_uuid_str: str | None = data.get('player_uuid')
    if player_uuid_str is None:
        await WebSocketUtils.send_error(websocket, 'get_ships', 'Field "player_uuid" is required')
    else:
        try:
            player_uuid: UUID = UUID(player_uuid_str)
        except ValueError:
            await WebSocketUtils.send_error(websocket, 'get_ships', 'Player UUID is not valid')
        else:
            player: Player | None = game.get_player_by_uuid(player_uuid)
            if player is None:
                await WebSocketUtils.send_error(websocket, 'get_ships', f'Player with UUID {player_uuid} not found')
            else:
                ships: list[Ship] = game.board.get_player_ships(player)
                response_data: list[dict] = []
                for ship in ships:
                    response_data.append({
                        'coord': {
                            'x': ship.coord.x,
                            'y': ship.coord.y
                        },
                        'color': player.color.value,
                        'size': ship.size,
                        'is_vertical': ship.is_vertical
                    })
                await websocket.send_json({'action': 'get_ships', 'status': 'ok', 'ships': response_data})
