from app.database.session import SessionLocal
from app.repositories.event_repository import event_repository

class EventService:

    def get_events(self):

        db = SessionLocal()

        try:

            return event_repository.get_all(db)

        finally:

            db.close()


event_service = EventService()