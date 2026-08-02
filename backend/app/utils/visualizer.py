import cv2

from app.schemas.detection import Detection

class Visualizer:

    def draw(self, image, detections):

        for detection in detections:

            x1,y1,x2,y2 = map(int,detection.bbox)

            cv2.rectangle(
                image,
                (x1,y1),
                (x2,y2),
                (0,255,0),
                2
            )

            label = f"{detection.class_name} {detection.confidence:.2f}"

            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )

        return image

visualizer = Visualizer()
