class IntrusionDetector:
    """
    Detects when a tracked person enters a restricted zone.

    A grace period is used because ByteTrack can temporarily
    lose a tracked object for a few frames.
    """

    def __init__(self, zone, margin=10, max_missing_frames=15):

        self.zone = zone
        self.margin = margin
        self.max_missing_frames = max_missing_frames

        # Tracks currently inside the restricted zone
        self.inside_tracks = set()

        # Number of consecutive frames each track has been missing
        self.missing_frames = {}

    def check(self, tracked_objects):

        events = []

        current_track_ids = set()

        for tracked_object in tracked_objects:

            track_id = tracked_object.track_id

            # Only detect persons
            if tracked_object.detection.class_name != "person":
                continue

            current_track_ids.add(track_id)

            # Track is visible again
            self.missing_frames[track_id] = 0

            center_x, center_y = (
                tracked_object.detection.bbox.center
            )

            inside = self.is_inside(
                center_x,
                center_y,
            )

            # --------------------------------
            # Person entered restricted zone
            # --------------------------------

            if (
                inside
                and track_id not in self.inside_tracks
            ):

                self.inside_tracks.add(track_id)

                events.append({
                    "track_id": track_id,
                    "event_type": "intrusion",
                    "severity": "CRITICAL",
                    "message": "Person entered restricted zone",
                })

            # --------------------------------
            # Person left restricted zone
            # --------------------------------

            elif (
                not inside
                and track_id in self.inside_tracks
            ):

                self.inside_tracks.remove(track_id)

                self.missing_frames.pop(
                    track_id,
                    None,
                )

        # --------------------------------
        # Handle temporarily missing tracks
        # --------------------------------

        missing_tracks = (
            self.inside_tracks - current_track_ids
        )

        for track_id in missing_tracks:

            self.missing_frames[track_id] = (
                self.missing_frames.get(track_id, 0)
                + 1
            )

            # Only forget the track after the
            # grace period has expired.
            if (
                self.missing_frames[track_id]
                >= self.max_missing_frames
            ):

                self.inside_tracks.remove(
                    track_id
                )

                self.missing_frames.pop(
                    track_id,
                    None,
                )

        return events

    def is_inside(self, x, y):

        x1, y1, x2, y2 = self.zone

        margin = self.margin

        return (
            x1 + margin <= x <= x2 - margin
            and
            y1 + margin <= y <= y2 - margin
        )

    def reset(self):
        """
        Clears all tracking state.
        Called when the camera starts a new session.
        """

        self.inside_tracks.clear()
        self.missing_frames.clear()