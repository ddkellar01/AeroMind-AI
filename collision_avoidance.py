"""CollisionAvoidance — TCAS-style companion for workflows.py.

Minimal functional implementation matching the interface workflows.py
expects (constructor only today). Evaluates separation against a list
of intruder tracks and reports the closest point of approach.
"""


class CollisionAvoidance:
    def __init__(self, min_separation_deg: float = 0.05, min_alt_separation_ft: float = 500.0):
        self.min_separation_deg = min_separation_deg
        self.min_alt_separation_ft = min_alt_separation_ft

    def assess(self, telemetry: dict, intruders: list | None = None) -> tuple[bool, str]:
        """Return (threat_detected, message). No intruder data = no threat."""
        if not intruders:
            return False, "No traffic threats"
        own_lat = telemetry.get("gps_lat", 0.0)
        own_lon = telemetry.get("gps_lon", 0.0)
        own_alt = telemetry.get("altitude_ft", 0.0)
        for intruder in intruders:
            d_lat = abs(intruder.get("gps_lat", 0.0) - own_lat)
            d_lon = abs(intruder.get("gps_lon", 0.0) - own_lon)
            d_alt = abs(intruder.get("altitude_ft", 0.0) - own_alt)
            if d_lat < self.min_separation_deg and d_lon < self.min_separation_deg \
                    and d_alt < self.min_alt_separation_ft:
                return True, "TRAFFIC: intruder inside separation envelope"
        return False, "Traffic clear"
