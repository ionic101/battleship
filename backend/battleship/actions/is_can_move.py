from typing import Any, TypeVar

from fastapi import WebSocket
from pydantic import ValidationError

from battleship.models.game import Game
from battleship.models.player import Player
from battleship.utils.websocket_utils import WebSocketUtils
from battleship.schemas.is_can_move import IsCanMoveScheme




T = TypeVar('T')


async def get_field(field_scheme: type[T], websocket: WebSocket, data: dict[str, Any]) -> T | None:
    try:
        return field_scheme(**data)
    except ValidationError as e:
        await WebSocketUtils.send_error(websocket, data['action'], e.errors()[0]['msg'])


# TODO: refactor
async def action_is_can_move(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    is_can_move_data: IsCanMoveScheme | None = await get_field(IsCanMoveScheme, websocket, data)
    if is_can_move_data is None:
        return
    player: Player = game.get_who_move()
    await websocket.send_json({
        'action': 'is_can_move',
        'can_move': player.uuid == is_can_move_data.player_uuid
    })