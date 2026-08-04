from ultralytics import YOLO
from app.core.logger import logger

class YOLODetector:
    def __init__(self, model_path: str= "yolo11n.pt"):
        logger.info("Loading YOLO model...")
        self.model = YOLO(model_path)
        logger.info("YOLO model loaded successfully!")

    def get_model(self):
        return self.model

#Singleton instance
detector = YOLODetector()