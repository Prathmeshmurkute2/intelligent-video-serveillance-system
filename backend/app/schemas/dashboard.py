from datetime import datetime
from typing import Any

from pydantic import BaseModel

class DashboardEvent(BaseModel):
    id:int
    event_type:str
    severity:str
    message:str
    timestamp:datetime
    camera_id:str
    event_metadata: dict[str, Any] | None = None


class DashboardAnalytics(BaseModel):
    total_events:int
    line_crossing:int
    instrusion:str
    people_detected:int
    vehicle_detection:int


class DashboardResponse(BaseModel):
    analytics: DashboardAnalytics
    recent_events: list[DashboardEvent]
    active_cameras:int
    active_alerts:int