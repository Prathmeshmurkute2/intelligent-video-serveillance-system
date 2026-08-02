from dataclasses import dataclass

from app.schemas.detection import Detection

@dataclass
class TrackedObject:
    track_id: int
    detection: Detection
