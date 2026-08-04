from app.database.session import SessionLocal
from app.repositories.event_repository import event_repository
from app.schemas.dashboard import (
    DashboardAnalytics,
    DashboardEvent,
    DashboardResponse,
)


class DashboardService:

    def get_dashboard(self):

        db = SessionLocal()

        try:

            recent_events = event_repository.get_recent(db)

            analytics = DashboardAnalytics(
                total_events=event_repository.count(db),
                line_crossings=event_repository.count_by_type(
                    db,
                    "line_crossing",
                ),
                intrusions=event_repository.count_by_type(
                    db,
                    "intrusion",
                ),
                people_detected=0,
                vehicles_detected=0,
            )

            events = [
                DashboardEvent.model_validate(event)
                for event in recent_events
            ]

            return DashboardResponse(
                analytics=analytics,
                recent_events=events,
                active_cameras=1,   # TODO: CameraRepository
                active_alerts=0,    # TODO: AlertRepository
            )

        finally:
            db.close()


dashboard_service = DashboardService()