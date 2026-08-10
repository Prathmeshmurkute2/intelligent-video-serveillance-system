from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(
        self,
        websocket: WebSocket,
    ):
        await websocket.accept()

        self.active_connections.append(websocket)

        print(
            f"🔌 WebSocket connected. "
            f"Clients: {len(self.active_connections)}"
        )

    def disconnect(
        self,
        websocket: WebSocket,
    ):
        if websocket in self.active_connections:

            self.active_connections.remove(websocket)

            print(
                f"🔌 WebSocket disconnected. "
                f"Clients: {len(self.active_connections)}"
            )

    async def broadcast(
        self,
        message: dict,
    ):

        print(
            f"📡 Broadcasting to "
            f"{len(self.active_connections)} client(s)"
        )

        disconnected = []

        for connection in self.active_connections:

            try:

                await connection.send_json(message)

                print("✅ Message sent successfully")

            except Exception as e:

                print(
                    f"❌ Failed to send WebSocket message: {e}"
                )

                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()