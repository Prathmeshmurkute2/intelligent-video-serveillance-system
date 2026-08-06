from pydantic import BaseModel


class MetricsResponse(BaseModel):
    fps: float
    processed_frames: int
    detected_objects: int
    generated_events: int
    uptime_seconds: float