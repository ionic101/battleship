from fastapi import WebSocket
from uuid import UUID, uuid4

from battleship.models.colors import Colors


class Player:
    def __init__(self, websocket: WebSocket, username: str) -> None:
        self.uuid: UUID = uuid4()
        self.websocket: WebSocket = websocket
        self.username: str = username
        self.color: Colors = Colors.AZURE
