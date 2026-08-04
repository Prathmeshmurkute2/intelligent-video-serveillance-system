from sqlalchemy.orm import Session
from sqlalchemy import func
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

    def get_all(self, db: Session,
                skip: int= 0,
                limit: int = 20):

        return (
            db.query(EventModel)
            .order_by(EventModel.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def count(self, db: Session):
        return db.query(func.count(EventModel.id)).scalar()

    def count_by_type(
        self,
        db: Session,
        event_type: str,
    ):
        return (
            db.query(func.count(EventModel.id))
            .filter(EventModel.event_type == event_type)
            .scalar()
        )

    
    def get_recent(
            self,
            db:Session,
            limit: int=10,
    ):
        return (
            db.query(EventModel)
            .order_by(EventModel.timestamp.desc())
            .limit(limit)
            .all()
        )
        
event_repository = EventRepository()