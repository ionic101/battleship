from uuid import UUID


from battleship.models.game import Game
from battleship.models.game import Game


class Manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self) -> None:
        self.lobbies: dict[UUID, Game] = {}
        self.games: list[Game] = []
    
    def create_game(self) -> Game:
        lobby: Game = Game()
        self.lobbies[lobby.uuid] = lobby
        return lobby
    
    def find_game(self, uuid: UUID) -> Game | None:
        return self.lobbies.get(uuid)
    
    


manager: Manager = Manager()
