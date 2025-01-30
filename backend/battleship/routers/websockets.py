from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from uuid import UUID
from battleship.schemas.player_join import PlayerJoin
from battleship.models.game import Game
from battleship.utils.manager import manager
from battleship.models.player import Player
from battleship.models.game_status import GameStatus
from battleship.models.ship import Ship

from battleship.utils.manager import manager
from typing import Any


ws_router: APIRouter = APIRouter(prefix='/ws')


async def send_error(websocket: WebSocket, action: str, message: str):
    await websocket.send_json({'action': action, 'status': 'error', 'message': message})


async def handle_join_game(websocket: WebSocket, game: Game, data: dict[str, Any]):
    username: str | None = data.get('username')
    if username is None:
        await send_error(websocket, 'join_game', 'Field "username" is required')
    else:
        new_player: Player = Player(websocket, username)
        game.add_player(new_player)
        await websocket.send_json({'action': 'join_game', 'player_uuid': str(new_player.uuid), 'status': 'ok'})
        await game.broadcast_without_player({'action': 'new_player', 'player': {'username': new_player.username, 'color': new_player.color.value}}, new_player)


async def handle_rejoin_game(websocket: WebSocket, game: Game, data: dict[str, Any]):
    player_uuid_str: str | None = data.get('player_uuid')
    if player_uuid_str is None:
        await send_error(websocket, 'rejoin_game', 'Field "player_uuid" is required')
    else:
        try:
            player_uuid: UUID = UUID(player_uuid_str)
        except ValueError:
            await send_error(websocket, 'rejoin_game', 'Player UUID is not valid')
        else:
            game.reconnect_player(player_uuid, websocket)
            await websocket.send_json({'action': 'rejoin_game', 'status': 'ok'})


async def handle_get_ships(websocket: WebSocket, game: Game, data: dict[str, Any]):
    if game.status != GameStatus.IN_GAME:
        await send_error(websocket, 'get_ships', 'Game not started')
    player_uuid_str: str | None = data.get('player_uuid')
    if player_uuid_str is None:
        await send_error(websocket, 'get_ships', 'Field "player_uuid" is required')
    else:
        try:
            player_uuid: UUID = UUID(player_uuid_str)
        except ValueError:
            await send_error(websocket, 'get_ships', 'Player UUID is not valid')
        else:
            player: Player | None = game.get_player_by_uuid(player_uuid)
            if player is None:
                await send_error(websocket, 'get_ships', f'Player with UUID {player_uuid} not found')
            else:
                ships: list[Ship] = game.board.get_player_ships(player)
                response_data: list[dict] = []
                for ship in ships:
                    response_data.append({
                        'coord': {
                            'x': ship.coord.x,
                            'y': ship.coord.y
                        },
                        'color': player.color.value,
                        'size': ship.size,
                        'is_vertical': ship.is_vertical
                    })
                await websocket.send_json({'action': 'get_ships', 'status': 'ok', 'ships': response_data})


@ws_router.websocket('/{lobby_id}')
async def websocket_endpoint(websocket: WebSocket, lobby_id: UUID):
    game: Game | None = manager.find_game(lobby_id)
    if game is None:
        await websocket.close()
        return
    
    await websocket.accept()
    try:
        while True:
            data: dict[str, Any] = await websocket.receive_json()
            action: str | None = data.get('action')

            match action:
                case 'get_status':
                    await websocket.send_json({'action': 'get_status', 'status': game.status.value})
                case 'join_game':
                    await handle_join_game(websocket, game, data)
                case 'rejoin_game':
                    await handle_rejoin_game(websocket, game, data)
                case 'get_players':
                    players_data: list[dict[str, str]] = [
                        {'username': player.username, 'color': player.color.value} for player in game.players
                    ]
                    await websocket.send_json({'action': 'get_players', 'players': players_data})
                case 'start_game':
                    game.start()
                    await game.broadcast({'action': 'start_game'})
                case 'get_ships':
                    await handle_get_ships(websocket, game, data)
    except WebSocketDisconnect:
        print(f"Client disconnected from lobby {lobby_id}")
