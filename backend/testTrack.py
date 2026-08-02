from app.tracking.tracker import tracker
import cv2

cap = cv2.VideoCapture("backend/app/videos/walk2.mp4")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    tracked_objects = tracker.track(frame)

    for obj in tracked_objects:
        print(
            obj.track_id,
            obj.detection.class_name,
            obj.detection.confidence
        )

    cv2.imshow("Tracking", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()