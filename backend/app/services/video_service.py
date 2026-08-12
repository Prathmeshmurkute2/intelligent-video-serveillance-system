import cv2
import asyncio
from datetime import datetime
from app.websocket.publisher import event_publisher

from app.core.config import settings
from app.core.logger import logger

from app.analytics.intrusion import IntrusionDetector

from app.tracking.tracker import tracker
from app.utils.visualizer import visualizer

from app.services.metrics_service import metrics_service
from app.services.event_service import event_service

from app.analytics.line_crossing import LineCrossingDetector

from app.schemas.event import Event

from app.database.session import SessionLocal


class VideoService:
    """
    Handles video capture, object tracking,
    analytics, visualization and frame streaming.
    """

    def __init__(self):
        self.cap = None
        self.event_loop = None

        # Horizontal virtual line.
        # Camera resolution is 1280x720,
        # so y=400 is currently used.
        self.line_crossing_detector = LineCrossingDetector(
            line_y=400
        )

        self.intrusion_detector = IntrusionDetector(
            zone=(400, 200, 900, 600)
        )

    # ---------------------------------------------------------
    # VIDEO
    # ---------------------------------------------------------

    def open_video(self, video_source=None):
        """
        Opens the configured video source.
        """

        source = video_source or settings.VIDEO_SOURCE

        # Convert "0" from environment variable to integer 0
        if isinstance(source, str) and source.isdigit():
            source = int(source)

        logger.info(
            "Opening video source: %s",
            source,
        )

        self.cap = cv2.VideoCapture(source)

        logger.info(
            "Camera opened: %s",
            self.cap.isOpened(),
        )

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

    # ---------------------------------------------------------
    # AI PIPELINE
    # ---------------------------------------------------------

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

        # -----------------------------------------------------
        # 1. YOLO + ByteTrack
        # -----------------------------------------------------

        tracked_objects = tracker.track(frame)

        print(
            "TRACKED:",
            [
                (
                    obj.track_id,
                    obj.detection.class_name,
                    obj.detection.bbox.center,
                )
                for obj in tracked_objects
            ],
        )
        intrusion_events = self.intrusion_detector.check(
            tracked_objects
        )

        if intrusion_events:

            logger.info(
                "🚨 INTRUSION EVENTS: %s",
                intrusion_events,
            )

            print(
                "🚨 INTRUSION:",
                intrusion_events,
            )

        # -----------------------------------------------------
        # 2. Metrics
        # -----------------------------------------------------

        metrics_service.processed_frames += 1

        metrics_service.detected_objects += len(
            tracked_objects
        )

        metrics_service.update_fps()

        # -----------------------------------------------------
        # 3. Analytics
        # -----------------------------------------------------

        events = self.process_analytics(
            tracked_objects
        )

        # -----------------------------------------------------
        # 4. Log detected events
        # -----------------------------------------------------

        if events:

            logger.info(
                "Analytics events detected: %s",
                events,
            )

            print(
                "🚨 EVENTS:",
                events,
            )

        # -----------------------------------------------------
        # 5. Draw detections
        # -----------------------------------------------------

        output = self.draw_frame(
            frame,
            tracked_objects,
        )

        return output

    # ---------------------------------------------------------
    # ANALYTICS + EVENT CREATION
    # ---------------------------------------------------------

    def process_analytics(self, tracked_objects):
        """
        Runs all analytics and creates surveillance events.
        """

        # --------------------------------
        # 1. Line crossing
        # --------------------------------

        line_events = self.line_crossing_detector.check(
            tracked_objects
        )

        # --------------------------------
        # 2. Intrusion detection
        # --------------------------------

        intrusion_events = self.intrusion_detector.check(
            tracked_objects
        )

        # Combine all analytics events
        analytics_events = (
            line_events + intrusion_events
        )

        if not analytics_events:
            return

        logger.info(
            "Analytics events detected: %s",
            analytics_events,
        )

        db = SessionLocal()

        try:

            for analytics_event in analytics_events:

                # --------------------------------
                # Determine event information
                # --------------------------------

                event_type = analytics_event["event_type"]

                if event_type == "intrusion":

                    severity = analytics_event.get(
                        "severity",
                        "CRITICAL",
                    )

                    message = analytics_event.get(
                        "message",
                        "Person entered restricted zone",
                    )

                    metadata = {
                        "zone": self.intrusion_detector.zone,
                    }

                else:

                    severity = "INFO"

                    message = "Person crossed gate"

                    metadata = {
                        "direction": analytics_event[
                            "direction"
                        ]
                    }

                # --------------------------------
                # Create Event
                # --------------------------------

                event = Event(
                    event_type=event_type,
                    track_id=analytics_event["track_id"],
                    camera_id="Gate-1",
                    timestamp=datetime.now(),
                    severity=severity,
                    message=message,
                    metadata=metadata,
                )

                # --------------------------------
                # Save + WebSocket broadcast
                # --------------------------------

                event_response = event_service.create_event(
                    db=db,
                    event=event,
                )

                logger.info(
                    "🚨 Event created successfully: %s",
                    event_response,
                )

        except Exception:

            logger.exception(
                "Failed to create surveillance event."
            )

        finally:

            db.close()

        return analytics_events
    # ---------------------------------------------------------
    # VISUALIZATION
    # ---------------------------------------------------------

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
            restricted_zone=self.intrusion_detector.zone,
        )

    # ---------------------------------------------------------
    # ENCODING
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # DESKTOP DISPLAY
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # CLEANUP
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # DESKTOP VIDEO PROCESSING
    # ---------------------------------------------------------

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

                self.display_frame(
                    output
                )

                if (
                    cv2.waitKey(1) & 0xFF
                    == ord("q")
                ):
                    break

        finally:

            self.cleanup()

    # ---------------------------------------------------------
    # FASTAPI STREAMING
    # ---------------------------------------------------------

    def generate_frames(
    self,
    video_source=None,
    event_loop=None,
):
        """
        Streams processed frames for FastAPI.
        """

        self.event_loop = event_loop

        self.open_video(video_source)

        try:

            while True:

                success, frame = self.read_frame()

                if not success:
                    break

                logger.info(
                    "Frame received: %s x %s",
                    frame.shape[1],
                    frame.shape[0],
                )

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
            self.event_loop = None

video_service = VideoService()