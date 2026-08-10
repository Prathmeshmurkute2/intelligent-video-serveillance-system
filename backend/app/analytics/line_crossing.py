class LineCrossingDetector:
    """
    Detects when a tracked object crosses a horizontal line.
    """

    def __init__(self, line_y: float):
        self.line_y = line_y
        self.previous_positions = {}

    def check(self, tracked_objects):

        events = []

        for tracked_object in tracked_objects:

            track_id = tracked_object.track_id

            x, y = tracked_object.detection.bbox.center

            previous_y = self.previous_positions.get(track_id)

            self.previous_positions[track_id] = y

            if previous_y is None:
                continue

            crossed = (
                previous_y < self.line_y
                and y >= self.line_y
            )

            if crossed:

                events.append({
                    "track_id": track_id,
                    "event_type": "line_crossing",
                    "direction": "IN",
                })

        return events