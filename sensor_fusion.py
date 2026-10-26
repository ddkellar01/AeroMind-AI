import numpy as np

class SensorFusionEngine:
    def __init__(self):
        self.last_alt = 5200.0
        self.alpha = 0.8  # Low-pass filter smoothing factor

    def fuse_sensors(self, raw_telemetry: dict) -> dict:
        # Apply basic complementary/low-pass filtering to eliminate jitter
        smoothed_alt = (self.alpha * self.last_alt) + ((1 - self.alpha) * raw_telemetry["altitude_ft"])
        self.last_alt = smoothed_alt
        
        filtered = raw_telemetry.copy()
        filtered["altitude_ft"] = round(smoothed_alt, 2)
        filtered["g_force"] = round(1.0 + abs(raw_telemetry["pitch_deg"]) / 90.0, 2)
        return filtered
