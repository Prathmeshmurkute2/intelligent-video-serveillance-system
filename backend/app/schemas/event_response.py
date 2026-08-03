from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

class EventResponse(BaseModel):

    id:int
    event_type: str
    track_id: int
    camera_id:str
    severity: str
    message:str
    timestamp: datetime
    event_metadata: dict[str, Any] | None = None

    model_config = ConfigDict(from_attribute=True)