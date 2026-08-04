from app.analytics.base import AnalyticsModule
from app.schemas.zone import Zone
from app.core.logger import logger


class InstrusionDetector(AnalyticsModule):

    def __init__(self):

        self.zone = Zone(
            x1=200,
            y1=150,
            x2=500,
            y2=450
        )

        self.altered_ids = set()

    def process(self, tracked_objects):

        for obj in tracked_objects:

            x,y = obj.detection.bbox.center

            if self.zone.contains(x,y):

                if obj.track_id not in self.altered_ids:

                    logger.info(
                        f"🚨 Intrusion! "
                        f"{obj.detection.class_name} "
                        f"#{obj.track_id}"
                    )

                    self.altered_ids.add(obj.track_id)

instrusion_detector = InstrusionDetector()