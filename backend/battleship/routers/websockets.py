from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from uuid import UUID
from battleship.schemas.player_join import PlayerJoin
from battleship.models.game import Game
from battleship.utils.manager import manager
from battleship.models.player import Player
from battleship.models.game_status import GameStatus
from battleship.models.ship import Ship
from battleship.models.shot_type import ShotType
from battleship.models.coord import Coord

from typing import TypeVar

from pydantic import BaseModel, ValidationError

from battleship.schemas.shot import ShotScheme

from battleship.utils.manager import manager
from typing import Any




T = TypeVar('T')


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

async def get_player_uuid(websocket: WebSocket, data: dict[str, Any]) -> UUID | None:
    player_uuid_str: str | None = data.get('player_uuid')
    if player_uuid_str is None:
        await send_error(websocket, 'shot', 'Field "player_uuid" is required')
        return None
    try:
        return UUID(player_uuid_str)
    except ValueError:
        await send_error(websocket, 'shot', 'Player UUID is not valid')


async def get_field(field_scheme: type[T], websocket: WebSocket, data: dict[str, Any]) -> T | None:
    try:
        return field_scheme(**data)
    except ValidationError as e:
        await send_error(websocket, data['action'], e.errors()[0]['msg'])


def get_response_shot_data(shot: ShotScheme) -> dict[str, Any]:



async def shot(websocket: WebSocket, game: Game, data: dict[str, Any]) -> None:
    shot_data: ShotScheme | None = await get_field(ShotScheme, websocket, data)
    if shot_data is None:
        return

    who_move: Player = game.get_who_move()
    if shot_data.player_uuid != who_move.uuid:
        await send_error(websocket, 'shot', f'Player with uuid {shot_data.player_uuid} can\'t move now')

    if shot_data.shot_coord in game.board.shots:
        await send_error(websocket, 'shot', f'Cell is not available for shot')
    
    game.board.shot(Coord(**shot_data.shot_coord.model_dump()))
    game.player_move()
    await websocket.send_json({'action': 'shot', 'status': 'ok'})
    await game.broadcast({'new_shot': 'shot', 'status': 'ok'})

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
                case 'get_shots':
                    response: list[dict[str, Any]] = []
                    for shot_coord in game.board.shots:
                        ship_data: dict[str, Any] = {
                            'type': game.board.shots[shot_coord],
                            'coord': {
                                'x': shot_coord.x,
                                'y': shot_coord.y
                            }
                        }
                        if game.board.shots[shot_coord] != ShotType.MISS:
                            ship_data['color'] = game.board.ships_coords[shot_coord].player.color.value
                        response.append(ship_data)
                    await websocket.send_json(response)
                case 'who_move':
                    player: Player = game.get_who_move()
                    await websocket.send_json({
                        'action': 'who_move',
                        'player': {
                            'username': player.username,
                            'color': player.color
                        }
                    })
                case 'shot':
                    await shot(websocket, game, data)
                    
    except WebSocketDisconnect:
        print(f"Client disconnected from lobby {lobby_id}")
