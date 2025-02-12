from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game


async def action_get_players(websocket: WebSocket, game: Game, **kwargs) -> None:
    players_data: list[dict[str, str]] = [
        {'username': player.username, 'color': player.color.value} for player in game.players
    ]
    await websocket.send_json({'action': 'get_players', 'status': 'ok', 'players': players_data})
