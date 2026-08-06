import cv2

from app.core.config import settings
from app.core.logger import logger
from app.detection.predictor import predictor
from app.tracking.tracker import tracker
from app.utils.visualizer import visualizer
from app.services.metrics_service import metrics_service


class VideoService:
    """
    Handles video capture, object detection,
    tracking, visualization and frame streaming.
    """

    def __init__(self):
        self.cap = None

    def open_video(self, video_source=None):
        """
        Opens the configured video source.
        """

        source = video_source or settings.VIDEO_SOURCE

        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            logger.error("Unable to open video source: %s", source)
            raise FileNotFoundError(
                f"Cannot open video source: {source}"
            )

        logger.info("Video source opened successfully.")

    def read_frame(self):
        """
        Reads the next frame.
        """
        return self.cap.read()

    def process_frame(self, frame):
        """
        Runs the complete AI pipeline.
        """

        # YOLO + Tracking
        tracked_objects = tracker.track(frame)

        metrics_service.processed_frames += 1

        metrics_service.detected_objects += len(tracked_objects)
        metrics_service.update_fps()
        # Analytics (line crossing, intrusion...)
        self.process_analytics(tracked_objects)

        # Draw detections
        output = self.draw_frame(frame, tracked_objects)

        return output

    def process_analytics(self, tracked_objects):
        """
        Runs analytics modules.

        Later this will call:

        - Line Counter
        - Intrusion Detection
        - Crowd Detection
        - Event Generation
        """

        # Example:
        # line_counter.update(tracked_objects)
        pass

    def draw_frame(self, frame, tracked_objects):
        """
        Draws bounding boxes, IDs and analytics.
        """

        return visualizer.draw(
            frame,
            tracked_objects,
        )

    def encode_frame(self, frame):
        """
        Converts frame into JPEG bytes.
        """

        success, buffer = cv2.imencode(".jpg", frame)

        if not success:
            logger.warning("Failed to encode frame.")
            return None

        return buffer.tobytes()

    def display_frame(self, frame):
        """
        Displays frame using OpenCV.
        """

        cv2.namedWindow(
            "Intelligent Video Surveillance",
            cv2.WINDOW_NORMAL,
        )

        cv2.resizeWindow(
            "Intelligent Video Surveillance",
            1280,
            720,
        )

        cv2.imshow(
            "Intelligent Video Surveillance",
            frame,
        )

    def cleanup(self):
        """
        Releases all resources.
        """

        if self.cap:
            self.cap.release()

        cv2.destroyAllWindows()

        logger.info("Video resources released.")

    def process_video(self, video_source=None):
        """
        Runs desktop OpenCV preview.
        """

        self.open_video(video_source)

        while True:

            success, frame = self.read_frame()

            if not success:
                break

            output = self.process_frame(frame)

            self.display_frame(output)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cleanup()

    def generate_frames(self, video_source=None):
        """
        Streams processed frames for FastAPI.
        """

        self.open_video(video_source)

        try:

            while True:

                success, frame = self.read_frame()

                if not success:
                    break

                output = self.process_frame(frame)

                frame_bytes = self.encode_frame(output)

                if frame_bytes is None:
                    continue

                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n"
                    + frame_bytes
                    + b"\r\n"
                )

        finally:

            self.cleanup()


video_service = VideoService()