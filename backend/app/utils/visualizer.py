import cv2

from app.analytics.line_counter import line_counter
from app.schemas.detection import Detection

class Visualizer:

    def draw(self, image, tracked_objects):

        for obj in tracked_objects:

            detection = obj.detection

            x1 = int(detection.bbox.x1)
            y1 = int(detection.bbox.y1)
            x2 = int(detection.bbox.x2)
            y2 = int(detection.bbox.y2)

            label = (
                f"{detection.class_name}"
                f"#{obj.track_id}"
                f"{detection.confidence:.2f}"
            )

            cv2.line(
                image,
                (0,300),
                (image.shape[1], 300),
                (0,0,255),
                2
            )

            cv2.rectangle(

                image,

                (x1,y1),

                (x2,y2),

                (0,255,0),

                2

            )



            cv2.putText(

                image,

                f"Cross Count: {line_counter.count}",

                (20, 40),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (0, 255, 255),

                2

            )


        return image

visualizer = Visualizer()
