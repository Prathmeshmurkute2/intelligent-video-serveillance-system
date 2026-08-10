from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    event_id: int = Field(
        validation_alias="id"
    )

    event_type: str

    track_id: int

    camera_id: str

    timestamp: datetime

    severity: str

    message: str

    metadata: dict = Field(
        validation_alias="event_metadata"
    )