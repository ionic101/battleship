from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game
from battleship.models.player import Player


# TODO: refactor
async def action_who_move(websocket: WebSocket, game: Game, **kwargs) -> None:
    player: Player = game.get_who_move()
    await websocket.send_json({
        'action': 'who_move',
        'player': {
            'username': player.username,
            'color': player.color.value
        }
    })
