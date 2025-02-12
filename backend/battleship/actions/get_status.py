from fastapi import WebSocket

from battleship.models.game import Game


async def action_get_status(websocket: WebSocket, game: Game, **kwargs) -> None:
    await websocket.send_json({'action': 'get_status', 'status': game.status.value})
