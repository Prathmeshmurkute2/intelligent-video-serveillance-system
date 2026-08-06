import cv2

from app.detection.predictor import predictor
from app.utils.visualizer import visualizer


class CameraService:

    def generate_frames(self):

        cap = cv2.VideoCapture("backend/app/videos/test.mp4")

        while True:

            success, frame = cap.read()

            if not success:
                break

            detections = predictor.predict(frame)

            output = visualizer.draw(frame, detections)

            ret, buffer = cv2.imencode(".jpg", output)

            frame_bytes = buffer.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )

        cap.release()


camera_service = CameraService()