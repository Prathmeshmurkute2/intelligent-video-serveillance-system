from dataclasses import dataclass

@dataclass
class BoundingBox:
    x1:float
    y1:float
    x2:float
    y2:float


    @property
    def center(self):
        return(
            (self.x1 + self.x2)/2,
            (self.y1+ self.y2)/2,
        )