from typing import List

import uvicorn
from fastapi import FastAPI, APIRouter

from battleship.routers import routers
from battleship.utils.config import config
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware



def bind_routers(app: FastAPI, routers: List[APIRouter]) -> None:
    for router in routers:
        app.include_router(router)


def get_app() -> FastAPI:
    app: FastAPI = FastAPI(title='Battleship API')
    bind_routers(app, routers)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Разрешить все домены
        allow_credentials=True,
        allow_methods=["*"],  # Разрешить все HTTP методы
        allow_headers=["*"],  # Разрешить все заголовки
    )
    return app


def main() -> None:
    uvicorn.run(
        'battleship.__main__:app',
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True
    )


app: FastAPI = get_app()

if __name__ == '__main__': 
    main()
