from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path: str= "yolo11n.pt"):
        print("Loading YOLO model...")
        self.model = YOLO(model_path)
        print("YOLO model loaded successfully!")

    def get_model(self):
        return self.model

#Singleton instance
detector = YOLODetector()