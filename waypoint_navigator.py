import math

class WaypointNavigator:
    def __init__(self, waypoints: list):
        self.waypoints = waypoints  # List of (lat, lon, alt)
        self.current_index = 0

    def get_current_target(self):
        if self.current_index < len(self.waypoints):
            return self.waypoints[self.current_index]
        return self.waypoints[-1]

    def update_position(self, current_lat, current_lon):
        target = self.get_current_target()
        dist = math.sqrt((target[0] - current_lat)**2 + (target[1] - current_lon)**2)
        # If within ~0.01 degrees (~1km), advance to next waypoint
        if dist < 0.01 and self.current_index < len(self.waypoints) - 1:
            self.current_index += 1
        return {"target_lat": target[0], "target_lon": target[1], "target_alt": target[2], "distance_remaining": dist}
