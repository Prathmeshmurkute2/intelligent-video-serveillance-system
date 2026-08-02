from app.detection.yolo import detector
from app.schemas.detection import Detection

class Predictor:

    def __init__(self):
        self.model = detector.get_model()

    def predict(self, image):
        results = self.model(image)

        detections = []

        for result in results:
            for box in result.boxes:

                detection = Detection(
                    class_id=int(box.cls),
                    class_name=result.names[int(box.cls)],
                    confidence=float(box.conf),
                    bbox=box.xyxy[0].tolist()
                )

                detections.append(detection)

        return detections

predictor = Predictor()