from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID
from battleship.models.game import Game
from battleship.utils.manager import manager
from battleship.utils.manager import manager
from typing import Any, Callable
from battleship.utils.websocket_utils import WebSocketUtils

from battleship.actions import *



ws_router: APIRouter = APIRouter(prefix='/ws')

async def send_status_game_not_found(websocket: WebSocket, game_id: UUID) -> None:
    await WebSocketUtils.send_error(websocket, 'connect', f'Game with UUID "{game_id}" not found')
    await websocket.close()


async def listen_websocket(websocket: WebSocket, game: Game) -> None:
    while True:
        data: dict[str, Any] = await websocket.receive_json()
        action: str | None = data.get('action')
        if action is None:
            await WebSocketUtils.send_error(websocket, 'error', 'error') # fix
            continue
        func: Callable | None = action_to_func.get(action)
        if func is None:
            await WebSocketUtils.send_error(websocket, 'error', 'error') # fix
            continue
        await func(websocket=websocket, game=game, data=data)


@ws_router.websocket('/{game_id}')
async def websocket_endpoint(websocket: WebSocket, game_id: UUID):
    game: Game | None = manager.find_game(game_id)
    
    if game is None:
        await send_status_game_not_found(websocket, game_id)
        return
    
    await websocket.accept()
    try:
        await listen_websocket(websocket, game)
    except WebSocketDisconnect:
        print(f"Client disconnected from lobby {game.uuid}")

# TODO: add typing of Callable
action_to_func: dict[str, Callable] = {
    'get_status': action_get_status,
    'join_game': action_join_game,
    'rejoin_game': action_rejoin_game,
    'get_players': action_get_players,
    'start_game': action_start_game,
    'get_ships': action_get_ships,
    'get_shots': action_get_shots,
    'who_move': action_who_move,
    'shot': action_shot,
    'is_can_move': action_is_can_move
}
