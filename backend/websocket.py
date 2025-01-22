import json

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, action: str, obj_type: str, data: dict):
        message = {"action": action, "type": obj_type, "data": data}
        message = json.dumps(message)
        for connection in self.active_connections:
            await connection.send_text(message)


ws = WebSocketManager()


async def handle_websocket(websocket: WebSocket):
    await ws.connect(websocket)
    try:
        while True:
            # Keep the connection open
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        ws.disconnect(websocket)
