from typing import Any

from fastapi import WebSocket

from battleship.models.game import Game


# TODO: refactor
async def action_start_game(game: Game, **kwargs) -> None:
    game.start()
    await game.broadcast({'action': 'start_game'})