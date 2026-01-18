from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    """Websocket connection handling class"""
    def __init__(self):
        """maps each document id to the list of users connected"""
        self.active_connections: Dict[int, List[WebSocket]] = {}
    

    async def connect(self, websocket: WebSocket, doc_id: int):
        """accepts the handshake and accepts users into a room"""
        await websocket.accept()

        if doc_id not in self.active_connections:
            self.active_connections[doc_id] = []
        self.active_connections[doc_id].append(websocket)
    

    def disconnect(self, websocket: WebSocket, doc_id: int):
        """removes a user and deletes and closes connection if room is empty"""
        self.active_connections[doc_id].remove(websocket)
        if not self.active_connections[doc_id]:
            del self.active_connections[doc_id]


    async def broadcast(self, message: str, doc_id: int):
        """Send data and control people room"""
        if doc_id in self.active_connections:
            for connection in self.active_connections[doc_id]:
                await connection.send_text(message)


manager = ConnectionManager()




