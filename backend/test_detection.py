import cv2

from app.utils.visualizer import visualizer
from app.detection.predictor import predictor


image=cv2.imread("images/person.jpg")

detections = predictor.predict(image)

output= visualizer.draw(image, detections)

cv2.imshow("Detections", output)

cv2.waitKey(0)

cv2.destroyAllWindows()