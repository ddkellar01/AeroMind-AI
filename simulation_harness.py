from earth_bridge import EarthFlightBridge

class SimulationHarness:
    def __init__(self):
        self.bridge = EarthFlightBridge()

    def inject_edge_case(self, scenario_type: str):
        if scenario_type == "microburst":
            print("🧪 Injecting simulation test: Sudden Wind Shear / Microburst")
            # Injects temporary down-draft telemetry signals
            return {"altitude_ft": 4000.0, "airspeed_kts": 90.0, "pitch_deg": -5.0}
        elif scenario_type == "sensor_drop":
            print("🧪 Injecting simulation test: Sensor Dropout Simulation")
            return None
        return None
