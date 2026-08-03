from sqlalchemy import Column, DateTime, Integer, String, JSON
from datetime import datetime

from app.database.base import Base


class EventModel(Base):

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)

    event_type = Column(String, nullable=False)

    track_id = Column(Integer, nullable=False)

    camera_id = Column(String, nullable=False)

    severity = Column(String, nullable=False)

    message = Column(String, nullable=False)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    event_metadata = Column(JSON)