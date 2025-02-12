from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.schemas.is_can_move import IsCanMoveScheme


async def action_is_can_move(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    is_can_move_data: IsCanMoveScheme | None = await WebSocketUtils.get_field(IsCanMoveScheme, websocket, data)
    if is_can_move_data is None:
        return
    player: Player = game.get_who_move()
    await websocket.send_json({
        'action': 'is_can_move',
        'can_move': player.uuid == is_can_move_data.player_uuid
    })
