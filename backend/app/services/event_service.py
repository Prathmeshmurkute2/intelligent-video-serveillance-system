from app.database.session import SessionLocal
from app.repositories.event_repository import event_repository

class EventService:

    def get_events(self, page:int, size:int):

        db = SessionLocal()

        try:
            skip = (page -1) * size

            return event_repository.get_all(
                db,
                skip=skip,
                limit=size,
                )

        finally:

            db.close()


event_service = EventService()