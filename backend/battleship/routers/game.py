from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from uuid import UUID
from battleship.schemas.player_join import PlayerJoin
from battleship.models.game import Game
from battleship.utils.manager import manager
from battleship.models.player import Player


game_router: APIRouter = APIRouter(prefix='/game')


@game_router.post('/create')
def create_game():
    game: Game = manager.create_game()
    return {
        'status': 'ok',
        'game_uuid': game.uuid
    }


# @game_router.post('/join/{uuid}')
# def join_game(uuid: UUID, player_data: PlayerJoin):
#     print(manager.lobbies)
#     game: Game | None = manager.find_game(uuid)
#     if game is None:
#         return HTTPException(status_code=404, detail=f'Game with uuid "{uuid}" not found')
#     player: Player = Player(
#         username=player_data.username,
#         color=player_data.color
#     )
#     game.add_player(player)
#     return {
#         'message': 'success'
#     }


# @game_router.websocket('/ws/')
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await websocket.send_text(f"Message received: {data}")
#     except WebSocketDisconnect:
#         print("Client disconnected")
