from dataclasses import dataclass
from app.schemas.bounding_box import BoundingBox


@dataclass
class Detection:
    class_id : int
    class_name: str
    confidence: float
    bbox: BoundingBox   

    