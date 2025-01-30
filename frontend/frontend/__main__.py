from typing import List

import uvicorn
from fastapi import FastAPI, APIRouter

from fastapi.responses import FileResponse

from frontend.utils.config import config



def bind_routers(app: FastAPI, routers: List[APIRouter]) -> None:
    for router in routers:
        app.include_router(router)


def get_app() -> FastAPI:
    app: FastAPI = FastAPI(title='Battleship')
    return app


def main() -> None:
    uvicorn.run(
        'frontend.__main__:app',
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True
    )


app: FastAPI = get_app()

@app.get('/')
def create_room():
    return FileResponse('frontend/pages/create_player.html')

@app.get('/join/{game_uuid}')
def join_room(game_uuid: str):
    return FileResponse('frontend/pages/create_player.html')

@app.get('/lobby')
def lobby_room():
    return FileResponse('frontend/pages/lobby.html')

@app.get('/play')
def play_room():
    return FileResponse('frontend/pages/game.html')

if __name__ == '__main__': 
    main()
