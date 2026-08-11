import cv2

from app.core.config import settings
from app.core.logger import logger
from app.tracking.tracker import tracker
from app.utils.visualizer import visualizer
from app.services.metrics_service import metrics_service
from app.analytics.line_crossing import LineCrossingDetector


class VideoService:
    """
    Handles video capture, object tracking,
    analytics, visualization and frame streaming.
    """

    def __init__(self):
        self.cap = None

        # Horizontal virtual line.
        # We will make this configurable later.
        self.line_crossing_detector = LineCrossingDetector(
            line_y=400
        )

    def open_video(self, video_source=None):
        """
        Opens the configured video source.
        """

        source = video_source or settings.VIDEO_SOURCE

        # Convert numeric camera source to integer
        if isinstance(source, str) and source.isdigit():
            source = int(source)

        logger.info(
            "Opening video source: %s",
            source,
        )

        self.cap = cv2.VideoCapture(source)

        logger.info("Camera opened: %s", self.cap.isOpened())

        if not self.cap.isOpened():

            logger.error(
                "Unable to open video source: %s",
                source,
            )

            raise FileNotFoundError(
                f"Cannot open video source: {source}"
            )

        logger.info(
            "Video source opened successfully."
        )

    def read_frame(self):
        """
        Reads the next frame.
        """

        if self.cap is None:
            return False, None

        return self.cap.read()

    def process_frame(self, frame):
        """
        Runs the complete AI pipeline.

        Pipeline:

        Frame
          ↓
        YOLO + ByteTrack
          ↓
        Tracked Objects
          ↓
        Analytics
          ↓
        Visualization
        """

        # --------------------------------
        # 1. YOLO + ByteTrack
        # --------------------------------

        tracked_objects = tracker.track(frame)

        print(
            "TRACKED:",
            [
                (
                    obj.track_id,
                    obj.detection.class_name,
                    obj.detection.detection if hasattr(obj.detection, "detection") else obj.detection.bbox.center
                )
                for obj in tracked_objects
            ]
        )
        # --------------------------------
        # 2. Metrics
        # --------------------------------

        metrics_service.processed_frames += 1

        metrics_service.detected_objects += len(
            tracked_objects
        )

        metrics_service.update_fps()

        # --------------------------------
        # 3. Analytics
        # --------------------------------

        events = self.process_analytics(
            tracked_objects
        )

        # --------------------------------
        # 4. Log detected events
        # --------------------------------

        if events:

            logger.info(
                "Analytics events detected: %s",
                events,
            )

            print(
                "🚨 EVENTS:",
                events,
            )

        # --------------------------------
        # 5. Draw detections
        # --------------------------------

        output = self.draw_frame(
            frame,
            tracked_objects,
        )

        return output

    def process_analytics(self, tracked_objects):
        """
        Runs analytics modules.

        Currently:
        - Line crossing detection

        Later:
        - Intrusion detection
        - Crowd detection
        - Loitering detection
        """

        events = []

        # -------------------------------
        # Line Crossing
        # -------------------------------

        line_events = self.line_crossing_detector.check(
            tracked_objects
        )

        events.extend(line_events)

        return events

    def draw_frame(
        self,
        frame,
        tracked_objects,
    ):
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

        success, buffer = cv2.imencode(
            ".jpg",
            frame,
        )

        if not success:

            logger.warning(
                "Failed to encode frame."
            )

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

        if self.cap is not None:

            self.cap.release()

            self.cap = None

        cv2.destroyAllWindows()

        logger.info(
            "Video resources released."
        )

    def process_video(self, video_source=None):
        """
        Runs desktop OpenCV preview.
        """

        self.open_video(video_source)

        try:

            while True:

                success, frame = self.read_frame()

                if not success:
                    break

                output = self.process_frame(
                    frame
                )

                self.display_frame(output)

                if (
                    cv2.waitKey(1) & 0xFF
                    == ord("q")
                ):
                    break

        finally:

            self.cleanup()

    def generate_frames(self, video_source=None):
        """
        Streams processed frames for FastAPI.
        """

        self.open_video(video_source)

        try:

            while True:

                success, frame = self.read_frame()
                if success:
                    logger.info(
                        "Frame received: %s x %s",
                        frame.shape[1],
                        frame.shape[0],
                    )
                if not success:
                    break

                output = self.process_frame(
                    frame
                )

                frame_bytes = self.encode_frame(
                    output
                )

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