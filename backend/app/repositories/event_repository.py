from sqlalchemy.orm import Session

from app.database.models import EventModel
from app.schemas.event import Event

class EventRepository:

    def create(
            self,
            db: Session,
            event: Event
    ):

        db_event = EventModel(
            event_type=event.event_type,
            track_id=event.track_id,
            camera_id=event.camera_id,
            severity=event.severity,
            message=event.message,
            timestamp=event.timestamp,
            event_metadata=event.metadata
        )

        db.add(db_event)

        db.commit()

        db.refresh(db_event)

        return db_event

    def get_all(self, db: Session):

        return (
            db.query(EventModel)
            .order_by(EventModel.timestamp.desc())
            .all()
        )
event_repository = EventRepository()