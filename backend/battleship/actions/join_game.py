from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.schemas.join_game import JoinGameScheme


async def action_join_game(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    join_game_data: JoinGameScheme | None = await WebSocketUtils.get_field(JoinGameScheme, websocket, data)
    if join_game_data is None:
        return
    
    new_player: Player = Player(websocket, join_game_data.username)
    game.add_player(new_player)
    await websocket.send_json({'action': 'join_game', 'player_uuid': str(new_player.uuid), 'status': 'ok'})
    await game.broadcast_without_player({'action': 'new_player', 'player': {'username': new_player.username, 'color': new_player.color.value}}, new_player)
