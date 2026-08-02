from dataclasses import dataclass

@dataclass
class Detection:
    class_id : int
    class_name: str
    confidence: float
    bbox: list[float]

    