import uuid
from typing import Any
from fastapi import WebSocket
from uuid import UUID

from battleship.models.player import Player
from battleship.models.ship import Ship
from battleship.models.game_status import GameStatus
from battleship.models.board import Board
from battleship.models.colors import Colors
from battleship.models.coord import Coord
from random import randint


class Game:
    def __init__(self) -> None:
        self.uuid: uuid.UUID = uuid.uuid4()
        self.players: list[Player] = []
        self.status: GameStatus = GameStatus.FREE
        self._free_colors: list[Colors] = list(Colors)

    def start(self) -> None:
        self.status = GameStatus.IN_GAME
        self.board: Board = Board(self.players)
        self.who_move_index: int = 0

    def stop(self) -> None:
        pass

    def get_usernames_players(self) -> list[str]:
        return list(map(lambda player: player.username, self.players))

    def add_player(self, player: Player) -> None:
        player.color = self._free_colors.pop(randint(0, len(self._free_colors) - 1))
        self.players.append(player)
    
    def get_player_by_uuid(self, player_uuid: UUID) -> Player | None:
        for player in self.players:
            if player.uuid == player_uuid:
                return player
        return None
    
    def get_who_move(self) -> Player:
        return self.players[self.who_move_index]
    
    async def player_move(self) -> None:
        self.who_move_index += 1
        if self.who_move_index >= len(self.players):
            self.who_move_index = 0
        player: Player = self.get_who_move()
        
        await self.broadcast(
            {'action': 'who_move',
                'player': {
                'username': player.username,
                'color': player.color.value}})
    
    async def broadcast(self, data: dict[str, Any]) -> None:
        for player in self.players:
            await player.websocket.send_json(data)
    
    async def broadcast_without_player(self, data: dict[str, Any], without_player: Player) -> None:
        for player in self.players:
            if player is without_player:
                continue
            await player.websocket.send_json(data)
