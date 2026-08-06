import time

from app.schemas.metrics import MetricsResponse


class MetricsService:

    def __init__(self):
        self.last_frame_time = time.time()
        self.start_time = time.time()
        self.processed_frames = 0
        self.detected_objects = 0
        self.generated_events = 0
        self.current_fps = 0.0

    def get_metrics(self):

        uptime = time.time() - self.start_time

        return MetricsResponse(
            fps=self.current_fps,
            processed_frames=self.processed_frames,
            detected_objects=self.detected_objects,
            generated_events=self.generated_events,
            uptime_seconds=uptime,
        )

    def update_fps(self):

        current = time.time()

        self.current_fps = 1 / (
            current - self.last_frame_time
        )

        self.last_frame_time = current
        
metrics_service = MetricsService()