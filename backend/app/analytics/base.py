from abc import ABC, abstractmethod

class AnalyticsModule(ABC):
    """
    Base class for every anlytics module.
    """

    @abstractmethod
    def process(self, tracked_objects):
        pass