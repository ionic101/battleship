from os import environ

from dotenv import load_dotenv


load_dotenv()


class Config():
    APP_HOST: str = environ.get('APP_HOST', '127.0.0.1')
    APP_PORT: int = int(environ.get('APP_PORT', 8000))
    BOARD_WIDTH: int = int(environ.get('BOARD_WIDTH', 30))
    BOARD_HEIGHT: int = int(environ.get('BOARD_HEIGHT', 30))


config: Config = Config()
