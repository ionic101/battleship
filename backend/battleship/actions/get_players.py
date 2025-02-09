from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game


# TODO: refactor
async def action_get_players(websocket: WebSocket, game: Game, data: dict[str, Any], **kwargs) -> None:
    players_data: list[dict[str, str]] = [
        {'username': player.username, 'color': player.color.value} for player in game.players
    ]
    await websocket.send_json({'action': 'get_players', 'players': players_data})
