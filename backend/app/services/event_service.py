from sqlalchemy.orm import Session

from app.repositories.event_repository import event_repository
from app.schemas.event_response import EventResponse


class EventService:

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