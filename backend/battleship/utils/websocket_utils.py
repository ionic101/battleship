from fastapi import WebSocket


class WebSocketUtils:
    @staticmethod
    async def send_error(websocket: WebSocket, action: str, message: str):
        await websocket.send_json({'action': action, 'status': 'error', 'message': message})
