from app.analytics.base import AnalyticsModule


class LineCounter(AnalyticsModule):
    """
    Counts objects crossing a horizontal virtual line.
    """

    def __init__(self, line_y: int):
        self.line_y = line_y
        self.previous_positions = {}
        self.crossed_ids = set()
        self.count = 0

    def process(self, tracked_objects):

        for obj in tracked_objects:

            track_id = obj.track_id

            _, current_y = obj.detection.bbox.center

            if track_id in self.previous_positions:

                previous_y = self.previous_positions[track_id]

                if (
                    previous_y < self.line_y
                    and current_y >= self.line_y
                    and track_id not in self.crossed_ids
                ):

                    self.count += 1
                    self.crossed_ids.add(track_id)

                    print(f"🚨 Object {track_id} crossed the line!")

            self.previous_positions[track_id] = current_y


# Singleton instance
line_counter = LineCounter(line_y=300)