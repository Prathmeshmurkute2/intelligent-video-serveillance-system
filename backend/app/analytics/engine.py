from typing import List

from app.analytics.base import AnalyticsModule
from app.analytics.line_counter import line_counter
from app.schemas.tracked_object import TrackedObject
from app.analytics.instrusion import instrusion_detector

class AnalyticsEngine:

    def __init__(self):

        self.modules: List[AnalyticsModule] = [
            line_counter,
            instrusion_detector
        ]

    def process(self, tracked_objects: List[TrackedObject]):

        for module in self.modules:
            module.process(tracked_objects)


analytics_engine = AnalyticsEngine()