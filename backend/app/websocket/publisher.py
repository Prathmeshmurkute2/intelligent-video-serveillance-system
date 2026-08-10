from app.websocket.manager import manager


class EventPublisher:

    async def publish_event(
        self,
        event_type: str,
        payload: dict,
    ):
        message = {
            "type": event_type,
            "data": payload,
        }

        print("📡 Broadcasting:", message)

        await manager.broadcast(message)


event_publisher = EventPublisher()