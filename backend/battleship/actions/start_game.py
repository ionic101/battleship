from typing import Any

from battleship.models.game import Game


async def action_start_game(game: Game, **kwargs) -> None:
    game.start()
    await game.broadcast({'action': 'start_game'})
