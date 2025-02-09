from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils



# TODO: refactor
async def action_join_game(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    username: str | None = data.get('username')
    if username is None:
        await WebSocketUtils.send_error(websocket, 'join_game', 'Field "username" is required')
    else:
        new_player: Player = Player(websocket, username)
        game.add_player(new_player)
        await websocket.send_json({'action': 'join_game', 'player_uuid': str(new_player.uuid), 'status': 'ok'})
        await game.broadcast_without_player({'action': 'new_player', 'player': {'username': new_player.username, 'color': new_player.color.value}}, new_player)
