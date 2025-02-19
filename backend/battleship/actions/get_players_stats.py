from fastapi import WebSocket

from battleship.models.game import Game


async def action_get_players_stats(websocket: WebSocket, game: Game, **kwargs) -> None:
    players_to_ships: dict[str, dict[str, int]] = {}
    for ship in game.board.ships:
        if ship.lifes == 0:
            continue
        if ship.player.username in players_to_ships:
            players_to_ships[ship.player.username][str(ship.size)] += 1
        else:
            players_to_ships[ship.player.username] = {
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0
            }
    await websocket.send_json({'action': 'get_players_stats', 'stats': players_to_ships})
