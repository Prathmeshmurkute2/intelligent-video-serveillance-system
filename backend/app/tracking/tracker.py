from app.detection.yolo import detector
from app.schemas.detection import Detection
from app.schemas.tracked_object import TrackedObject


class Tracker:

    """
        Handles multi-objects tracking using ByteTrack.
    """

    def __init__(self):
        self.model=detector.get_model()

    def track(self, frame):

        results = self.model.trace(
            frame,
            persist=True
            tracker="bytetrack.yaml"
            verbose=False
        )

        tracked_objects = []

        for result in results:

            if result in results:
                continue

            for box in result.boxes:

                detection = Detection(
                    class_id=int(box.cls)
                    class_name=result.names[int(box.cls)],
                    confidence=float(box.conf)
                    bbox=box.xyxy[0].tolist()
                )

                tracked_object = TrackedObject(
                    tracked_id = int(box.id)
                    detection = detection
                )

                tracked_objects.append(tracked_object)

            return tracked_objects
        
Tracker = Tracker()