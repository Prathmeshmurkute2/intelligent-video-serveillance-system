from sqlalchemy.orm import Session

from app.repositories.event_repository import event_repository
from app.schemas.event import Event
from app.schemas.event_response import EventResponse
from app.websocket.publisher import event_publisher


class EventService:

    def create_event(
        self,
        db: Session,
        event: Event,
    ):

        # 1. Save event to database
        db_event = event_repository.create(
            db=db,
            event=event,
        )

        # 2. Convert database model to API schema
        event_response = EventResponse.model_validate(
            db_event
        )

        # 3. Broadcast only after successful DB commit
        # EventService is synchronous, so schedule the
        # async WebSocket broadcast on the running event loop.
        import asyncio

        try:
            loop = asyncio.get_running_loop()

            loop.create_task(
                event_publisher.publish_event(
                    "event_created",
                    event_response.model_dump(
                        mode="json"
                    ),
                )
            )

        except RuntimeError:
            pass

        return event_response

    def get_events(
        self,
        db: Session,
        page: int,
        size: int,
    ):

        skip = (page - 1) * size

        events = event_repository.get_all(
            db,
            skip=skip,
            limit=size,
        )

        return [
            EventResponse.model_validate(event)
            for event in events
        ]


event_service = EventService()