from battleship.models.ship import Ship
from battleship.models.coord import Coord
from battleship.models.shot_type import ShotType
from battleship.models.player import Player
from random import choice


size_to_count_ships: dict[int, int] = {
    1: 4,
    2: 3,
    3: 2,
    4: 1
}
start_coord: Coord = Coord(0, 0)
end_coord: Coord = Coord(29, 29)


class Board:
    def __init__(self, players: list[Player]) -> None:
        self.ships_coords: dict[Coord, Ship] = {}
        self.ships: list[Ship] = []
        self.shots: dict[Coord, ShotType] = {}
        self.generate_board(players)
    
    def __is_ship_possible(self, coord: Coord, size: int, is_vertical: bool) -> bool:
        if coord in self.ships_coords:
            return False
        for d in range(size):
            d_coord: Coord = Coord(0, d) if is_vertical else Coord(d, 0)
            new_coord: Coord = coord + d_coord
            if new_coord in self.ships_coords or new_coord.x < start_coord.x or new_coord.y < start_coord.y or new_coord.x > end_coord.x or new_coord.y > end_coord.y:
                return False
        return True
    
    def __generate_ship_in_random(self, player: Player, size: int) -> Ship:
        while True:
            random_coord: Coord = Coord.get_random(start_coord, end_coord)
            is_vertical: bool = choice([True, False])
            if self.__is_ship_possible(random_coord, size, is_vertical):
                return Ship(player, random_coord, size, is_vertical)
            if self.__is_ship_possible(random_coord, size, not is_vertical):
                return Ship(player, random_coord, size, not is_vertical)
    
    def __add_coords_shipt_to_board(self, ship: Ship) -> None:
        for d in range(ship.size):
            d_coord: Coord = Coord(0, d) if ship.is_vertical else Coord(d, 0)
            cur_coord: Coord = ship.coord + d_coord
            self.ships_coords[cur_coord] = ship
    
    def generate_board(self, players: list[Player]):
        for player in players:
            for size, count in size_to_count_ships.items():
                for _ in range(count):
                    ship: Ship = self.__generate_ship_in_random(player, size)
                    self.__add_coords_shipt_to_board(ship)
                    self.ships.append(ship)
    
    def get_player_ships(self, player: Player) -> list[Ship]:
        return list(filter(lambda ship: ship.player == player, self.ships))
