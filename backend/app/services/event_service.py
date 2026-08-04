from app.database.session import SessionLocal
from app.repositories.event_repository import event_repository
from sqlalchemy.orm import Session

class EventService:

    def get_events(self,
                   db:Session,
                    page:int,
                      size:int,
                      ):

        #db = SessionLocal()

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