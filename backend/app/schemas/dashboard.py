from datetime import datetime
from typing import Any

from pydantic import BaseModel
from pydantic import BaseModel, ConfigDict

class DashboardEvent(BaseModel):
    id: int
    event_type: str
    severity: str
    message: str
    timestamp: datetime
    camera_id: str
    event_metadata: dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True)

class DashboardAnalytics(BaseModel):
    total_events: int
    line_crossings: int
    intrusions: int
    people_detected: int
    vehicles_detected: int


class DashboardResponse(BaseModel):
    analytics: DashboardAnalytics
    recent_events: list[DashboardEvent]
    active_cameras: int
    active_alerts: int