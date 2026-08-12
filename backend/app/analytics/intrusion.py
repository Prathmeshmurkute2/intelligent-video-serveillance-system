class IntrusionDetector:
    """
    Detects when a tracked person enters a restricted zone.
    """

    def __init__(self, zone):
        self.zone = zone
        self.inside_tracks = set()

    def check(self, tracked_objects):

        events = []

        for tracked_object in tracked_objects:

            track_id = tracked_object.track_id

            # We currently track only persons,
            # but keep this check for safety.
            if tracked_object.detection.class_name != "person":
                continue

            center_x, center_y = (
                tracked_object.detection.bbox.center
            )

            inside = self.is_inside(
                center_x,
                center_y,
            )

            # Person entered the zone
            if inside and track_id not in self.inside_tracks:

                self.inside_tracks.add(track_id)

                events.append({
                    "track_id": track_id,
                    "event_type": "intrusion",
                    "severity": "CRITICAL",
                    "message": "Person entered restricted zone",
                })

            # Person left the zone
            elif not inside and track_id in self.inside_tracks:

                self.inside_tracks.remove(track_id)

        return events

    def is_inside(self, x, y):

        x1, y1, x2, y2 = self.zone

        return (
            x1 <= x <= x2
            and
            y1 <= y <= y2
        )