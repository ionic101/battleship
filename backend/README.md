#### Создание игрока
```
Client:
{
    "action": "get_status"
}
Server:
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



Client:
{
    "action": "get_players"
}
Server:
{
    "action": "get_players",
    "players": [
        {
            'username': 'player1',
            'color': '#FF0000'
        },
        {
            'username': 'player2',
            'color': '#00FF00'
        }
    ]
}



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
Client:
{
    "action": "rejoin_game",
    "player_uuid": {player_uuid}
}
Server:
{
    'action': 'rejoin_game',
    'status': 'error',
    'message': 'Field "player_uuid" is required'
}
{
    'action': 'rejoin_game',
    'status': 'error',
    'message': 'Player UUID is not valid'
}
{
    'action': 'rejoin_game',
    'status': 'ok'
}


Client:
{
    'action': 'get_ships',
    'player_uuid': 'player_uuid',
}
Server:
{
    'action': 'get_ships',
    'status': 'ok',
    'ships': [
        {
            'coord': {
                'x': 0,
                'y': 0
            },
            'color': '#00FF00',
            'size': 3,
            'is_vertical': False
        }
    ]
}


Client:
{
    'action': 'shot',
    'player_uuid': player_uuid,
    'shot': {
        'x': 0,
        'y': 0
    }
}
Server:
{
    'action': 'shot',
    'status': 'ok'
}



Client:
{
    'action': 'get_shots'
}
Server:
{
    'action': 'get_shots',
    'shots': [
        {
            'type': 'miss',
            'coord: {
                'x': 0,
                'y': 0
            }
        },
         {
            'type': 'hit',
            'color': '',
            'coord: {
                'x': 0,
                'y': 0
            }
        },
        {
            'type': destroy,
            'color': '',
            'coord: {
                'x': 0,
                'y': 0
            }
        }
    ]
}
