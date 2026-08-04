from datetime import datetime
import uuid

from app.database.session import SessionLocal
from app.repositories.event_repository import event_repository
from app.schemas.event import Event
from app.core.logger import logger

db = SessionLocal()

event = Event(
    event_id=str(uuid.uuid4()),
    event_type="line_crossing",
    track_id=1,
    camera_id="Gate-1",
    severity="INFO",
    message="Person crossed gate",
    timestamp=datetime.now(),
    metadata={
        "direction": "IN"
    }
)

event_repository.create(db, event)

db.close()

logger.info("Saved successfully!")