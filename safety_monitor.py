class SafetyMonitor:
    def __init__(self, min_alt=500.0, max_g=3.5, min_speed=60.0):
        self.min_alt = min_alt
        self.max_g = max_g
        self.min_speed = min_speed

    def check_envelope(self, telemetry: dict) -> tuple[bool, str]:
        if telemetry["altitude_ft"] < self.min_alt:
            return False, "CRITICAL: Terrain proximity warning! Minimum altitude breached."
        if telemetry["airspeed_kts"] < self.min_speed:
            return False, "CRITICAL: Near stall speed detected! Pitch down required."
        if telemetry.get("g_force", 1.0) > self.max_g:
            return False, "CRITICAL: Excessive G-Force limit exceeded."
        return True, "Nominal"

    def generate_override_commands(self) -> dict:
        # Hard-coded safe recovery response if envelope is violated
        return {
            "thought_process": "SAFETY OVERVWRITE: Recovering aircraft from unsafe envelope envelope.",
            "elevator": -0.5,  # Push nose down to clear stall/terrain
            "aileron": 0.0,
            "rudder": 0.0,
            "throttle": 1.0   # Full power climb/escape
        }
