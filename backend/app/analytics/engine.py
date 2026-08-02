from app.analytics.line_counter import line_counter

class AnalyticsEngine:

    """
        Runs all analytics modules.
    """

    def __init__(self):
        self.modules = [
            line_counter
        ]

    def process(self, tracked_objects):
        for module in self.modules:
            module.process(tracked_objects)

Analytics_engine = AnalyticsEngine()