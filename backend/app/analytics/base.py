from abc import ABC, abstractmethod
from typing import List

from app.schemas.tracked_object import TrackedObject

class AnalyticsModule(ABC):
    """
    Base class for every anlytics module.
    """

    @abstractmethod
    def process(self, tracked_objects: List[TrackedObject])->None:
        """
        Process tracked objects.
        """
        pass