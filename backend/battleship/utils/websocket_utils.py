from typing import TypeVar, Any

from fastapi import WebSocket
from pydantic import ValidationError


class WebSocketUtils:
    T = TypeVar('T')

    @staticmethod
    async def send_error(websocket: WebSocket, action: str, message: str):
        await websocket.send_json({'action': action, 'status': 'error', 'message': message})

    @staticmethod
    async def get_field(field_scheme: type[T], websocket: WebSocket, data: dict[str, Any]) -> T | None:
        try:
            return field_scheme(**data)
        except ValidationError as e:
            await WebSocketUtils.send_error(websocket, data['action'], e.errors()[0]['msg'])
