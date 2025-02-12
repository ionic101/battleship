from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.schemas.rejoin_game import RejoinGameScheme


async def action_rejoin_game(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    rejoin_game_data: RejoinGameScheme | None = await WebSocketUtils.get_field(RejoinGameScheme, websocket, data)
    if rejoin_game_data is None:
        return
    player: Player | None = game.get_player_by_uuid(rejoin_game_data.player_uuid)
    if player is None:
        await WebSocketUtils.send_error(websocket, 'rejoin_game', f'Plyaer with UUID "{rejoin_game_data.player_uuid}" does not exist')
        return
    player.websocket = websocket
    await websocket.send_json({'action': 'rejoin_game', 'status': 'ok'})
