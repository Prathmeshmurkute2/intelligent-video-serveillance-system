from app.websocket.manager import manager


class EventPublisher:

    async def broadcast(self, message: dict):

        disconnected = []

        for connection in self.active_connections:

            try:
                await connection.send_json(message)

            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


event_publisher = EventPublisher()