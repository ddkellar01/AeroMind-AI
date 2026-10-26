"""VisionMapper — terrain / horizon mapping companion for workflows.py.

Minimal functional implementation matching the interface workflows.py
expects (constructor only today). Maps telemetry onto a coarse local
grid so later vision work has a stable API to build on.
"""


class VisionMapper:
    def __init__(self, grid_resolution_deg: float = 0.01):
        self.grid_resolution_deg = grid_resolution_deg
        self.last_frame = None

    def map_frame(self, telemetry: dict) -> dict:
        """Return a coarse position cell for the current telemetry fix."""
        lat = telemetry.get("gps_lat", 0.0)
        lon = telemetry.get("gps_lon", 0.0)
        cell = (
            round(lat / self.grid_resolution_deg),
            round(lon / self.grid_resolution_deg),
        )
        self.last_frame = {
            "cell": cell,
            "altitude_ft": telemetry.get("altitude_ft", 0.0),
            "heading_deg": telemetry.get("heading_deg", 0.0),
        }
        return self.last_frame
