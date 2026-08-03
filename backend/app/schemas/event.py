from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    event_id: str
    event_type:str
    track_id:int
    camera_id: str
    timestamp:datetime
    severity:str
    message:str
    metadata: dict