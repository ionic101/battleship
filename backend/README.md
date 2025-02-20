#### Подключение по WebSocket
Server:
```
{
    "action": "websocket",
    "status": "ok"
}
```


#### Создание игрока
Client:
```
{
    "action": "get_status"
}
```
Server:
```
{
    "action": "get_status",
    "status": "free"
}
{
    "action": "get_status",
    "status": "full"
}
{
    "action": "get_status",
    "status": "in_game"
}
```


#### Лобби
```
Client:
{
    "action": "join_game",
    "username": "player1"
}
Server:
{
    "action": "join_game",
    "status": "ok"
}
{
    "action": "join_game",
    "status": "error",
    "message": "message"
}
```

#### Получение списка игроков
```
Client:
{
    "action": "get_players"
}
Server:
{
    "action": "get_players",
    "status": "ok",
    "players": [
        {
            "username": "player1",
            "color": "#FF0000"
        },
        {
            "username": "player2",
            "color": "#00FF00"
        }
    ]
}
```

```
Client:
{
    "action": "start_game"
}
Server:
{
    "action": "start_game"
}



Server:
{
    "action": "new_player",
    "player": {
        "username": "player1",
        "color": "#00FF00"
    }
}
```


#### Игра
```
Client:
{
    "action": "rejoin_game",
    "player_uuid": {player_uuid}
}
Server:
{
    "action": "rejoin_game",
    "status": "error",
    "message": "Field "player_uuid" is required"
}
{
    "action": "rejoin_game",
    "status": "error",
    "message": "Player UUID is not valid"
}
{
    "action": "rejoin_game",
    "status": "ok"
}
```

#### Получение списка кораблей
```
Client:
{
    "action": "get_ships",
    "player_uuid": "player_uuid",
}
Server:
{
    "action": "get_ships",
    "status": "ok",
    "ships": [
        {
            "coord": {
                "x": 0,
                "y": 0
            },
            "color": "#00FF00",
            "size": 3,
            "is_vertical": False
        }
    ]
}
```

Client:
{
    "action": "shot",
    "player_uuid": player_uuid,
    "shot_coord": {
        "x": 0,
        "y": 0
    }
}
Server:
{
    "action": "shot",
    "status": "ok"
}
{
    "action": "shot",
    "status": "error",
    "message": "Player with uuid can"t move now"
}



Client:
{
    "action": "get_shots"
}
Server:
{
    "action": "get_shots",
    "shots": [
        {
            "type": "miss",
            "coord: {
                "x": 0,
                "y": 0
            }
        },
         {
            "type": "hit",
            "color": "#8A2BE2",
            "coord: {
                "x": 0,
                "y": 0
            }
        },
        {
            "type": "destroy",
            "color": "#BFFF00",
            "coord: {
                "x": 0,
                "y": 0
            }
        }
    ]
}



Server:
{
    "action": "new_shot",
    "shot": {
        "type": "miss",
        "coord: {
            "x": 0,
            "y": 0
        }
    }
}
{
    "action": "new_shot",
    "shot": {
        "type": "hit",
        "color": "#8A2BE2",
        "coord: {
            "x": 0,
            "y": 0
        }
    }
}
{
    "action": "new_shot",
    "shot": {
        "type": "destroy",
        "color": "#BFFF00",
        "coord: {
            "x": 0,
            "y": 0
        }
    }
}



Client:
{
    "action": "who_move"
}
Server:
{
    "action": "who_move",
    "player": {
        "username": "player1",
        "color": "#BFFF00"
    }
}


Client:
{
    "action": "is_can_move",
    "player_uuid": player_uuid
}
Server:
{
    "action": "is_can_move",
    "can_move": true
}

#### Получение статистики игроков
Client:
```
{
    "action": "get_players_stats"
}
```
Server:
{
    "action: "get_players_stats",
    "stats": {
        "player1": {
            "color": "#BFFF00",
            "ships": {
                "1": 3,
                "2": 0,
                "3": 1,
                "4": 1
            }
        }
    }
}