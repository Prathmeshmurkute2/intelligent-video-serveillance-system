from typing import List

from app.database.session import SessionLocal
from app.repositories.event_repository import event_repository
from app.schemas.event import Event

class EventManager:

    def __init__(self):
        self.events: List[Event]=[]

    def publish(self, event: Event):

        db = SessionLocal()

        try:
            event_repository.create(db, event)

            self.events.append(event)

        finally:

            db.close()


event_manager = EventManager()