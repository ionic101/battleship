from typing import Any
from uuid import UUID

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils



# TODO: refactor
async def action_rejoin_game(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    player_uuid_str: str | None = data.get('player_uuid')
    if player_uuid_str is None:
        await WebSocketUtils.send_error(websocket, 'rejoin_game', 'Field "player_uuid" is required')
    else:
        try:
            player_uuid: UUID = UUID(player_uuid_str)
        except ValueError:
            await WebSocketUtils.send_error(websocket, 'rejoin_game', 'Player UUID is not valid')
        else:
            game.reconnect_player(player_uuid, websocket)
            await websocket.send_json({'action': 'rejoin_game', 'status': 'ok'})
