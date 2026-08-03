import cv2

from app.detection.predictor import predictor
from app.utils.visualizer import visualizer
from app.tracking.tracker import tracker


class VideoService:
    """
    Handles video processing and visualization.
    """

    def process_video(self, video_path: str):

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        while True:

            ret, frame = cap.read()

            if not ret:
                break

            # detections = predictor.predict(frame)

            # output = visualizer.draw(frame, detections)
            
            tracked_objects = tracker.track(frame)

            output = visualizer.draw(frame, tracked_objects)

            cv2.namedWindow(
                "Intelligent Video Surveillance",
                cv2.WINDOW_NORMAL
            )

            cv2.resizeWindow(
                "Intelligent Video Surveillance",
                1280,
                720
            )

            cv2.imshow("Intelligent Video Surveillance", output)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # These should be OUTSIDE the while loop
        cap.release()
        cv2.destroyAllWindows()


video_service = VideoService()