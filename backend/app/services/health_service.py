import cv2
from sqlalchemy import text

from app.core.config import settings
from app.database.session import SessionLocal
from app.schemas.health import HealthResponse


class HealthService:

    def get_health(self):

        database = "disconnected"

        try:
            db = SessionLocal()

            db.execute(text("SELECT 1"))

            database = "connected"

        except Exception:
            database = "disconnected"

        finally:
            db.close()

        camera = "unavailable"

        cap = cv2.VideoCapture(settings.VIDEO_SOURCE)

        if cap.isOpened():
            camera = "available"

        cap.release()

        return HealthResponse(
            status="healthy",
            version=settings.APP_VERSION,
            database=database,
            model="loaded",
            camera=camera,
        )


health_service = HealthService()