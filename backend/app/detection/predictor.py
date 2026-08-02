from app.detection.yolo import detector

class Predictor:

    def __init__(self):
        self.model = detector.get_model()

    def predict(self, image):
        results = self.model(image)
        return results

predictor = Predictor()