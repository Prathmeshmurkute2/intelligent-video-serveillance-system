from dataclasses import dataclass

@dataclass
class Zone:
    x1: int
    y1: int
    x2: int
    y2: int

    def contains(self, x: float, y: float) -> bool:
        return (
            self.x1 <= x <= self.x2
            and
            self.y1<= y <= self.y2
        )