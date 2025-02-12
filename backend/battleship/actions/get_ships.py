from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.models.game_status import GameStatus
from battleship.models.ship import Ship
from battleship.schemas.get_ships import GetShipsScheme


async def action_get_ships(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    if game.status != GameStatus.IN_GAME:
        await WebSocketUtils.send_error(websocket, 'get_ships', 'Game not started')
        return
    
    get_ships_data: GetShipsScheme | None = await WebSocketUtils.get_field(GetShipsScheme, websocket, data)
    if get_ships_data is None:
        return
    
    player: Player | None = game.get_player_by_uuid(get_ships_data.player_uuid)
    if player is None:
        await WebSocketUtils.send_error(websocket, 'get_ships', f'Player with UUID {get_ships_data.player_uuid} not found')
        return
    
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
