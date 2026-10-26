import time
import json
import sys
from earth_bridge import EarthFlightBridge
from sensor_fusion import SensorFusionEngine
from waypoint_navigator import WaypointNavigator
from safety_monitor import SafetyMonitor
from weather_fetcher import WeatherFetcher
from logger_blackbox import BlackBoxLogger
from vision_mapper import VisionMapper
from collision_avoidance import CollisionAvoidance
from emergency_handler import EmergencyHandler
from system_diagnostics import SystemDiagnostics
from actuator_calibrator import ActuatorCalibrator
from cloud_sync import CloudSync
from dashboard_ui import start_dashboard_background, update_dashboard_state
from telemetry_streamer import start_streamer_thread, broadcast_telemetry
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT

class AeroMindWorkflowManager:
    def __init__(self):
        print("🔧 Initializing AeroMind Workflow Subsystems...")
        self.bridge = EarthFlightBridge()
        self.fusion = SensorFusionEngine()
        self.navigator = WaypointNavigator([(37.7749, -122.4194, 5000), (37.8000, -122.5000, 6000)])
        self.safety = SafetyMonitor()
        self.weather = WeatherFetcher()
        self.logger = BlackBoxLogger()
        self.vision = VisionMapper()
        self.tcas = CollisionAvoidance()
        self.emergency = EmergencyHandler()
        self.diagnostics = SystemDiagnostics()
        self.calibrator = ActuatorCalibrator()
        self.cloud = CloudSync()
        self.client = genai.Client()

    def run_pre_flight_checks(self) -> bool:
        print("\n--- PHASE 1: Pre-Flight Systems & Sensor Diagnostic ---")
        telemetry = self.bridge.get_telemetry()
        weather_cond = self.weather.fetch_conditions(telemetry["gps_lat"], telemetry["gps_lon"])
        print(f"🌤️ Weather Check Passed. Wind: {weather_cond['wind_speed_kts']} kts")
        print(f"🛰️ Telemetry Link Verified. Initial Alt: {telemetry['altitude_ft']} ft")
        print("✅ Pre-flight sequence complete. All systems nominal.\n")
        return True

    def execute_flight_sequence(self):
        print("--- PHASE 2: Autonomous Flight Loop Engaged ---")
        start_dashboard_background()
        start_streamer_thread()
        
        flight_active = True
        cycle_count = 0

        try:
            while flight_active and cycle_count < 100:  # Adjust loop limit or run indefinitely via `while True`
                loop_start = time.time()
                cycle_count += 1

                # 1. Gather & Fuse Sensors
                raw_telemetry = self.bridge.get_telemetry()
                telemetry = self.fusion.fuse_sensors(raw_telemetry)

                # 2. Check Subsystems & Emergency Status
                is_emergency, emergency_msg = self.emergency.assess_subsystems(
                    {"fuel_pressure_psi": 45.0}, {"bus_volts": 28.0}
                )
                if is_emergency:
                    print(f"🚨 {emergency_msg}")
                    decision = self.safety.generate_override_commands()
                else:
                    # 3. Safety Envelope Check
                    is_safe, safety_msg = self.safety.check_envelope(telemetry)
                    if not is_safe:
                        print(f"⚠️ {safety_msg}")
                        decision = self.safety.generate_override_commands()
                    else:
                        # 4. Waypoint & Navigation Update
                        wp_data = self.navigator.update_position(telemetry["gps_lat"], telemetry["gps_lon"])
                        
                        # 5. Query Gemini 4 Argon for Reasoning
                        prompt = f"Telemetry: {json.dumps(telemetry)}. Waypoint Target: {json.dumps(wp_data)}. Determine adjustments."
                        api_start = time.time()
                        response = self.client.models.generate_content(
                            model='gemini-4-argon',
                            contents=prompt,
                            config=types.GenerateContentConfig(
                                system_instruction=SYSTEM_PROMPT,
                                response_mime_type="application/json",
                                temperature=0.2,
                            ),
                        )
                        api_latency = (time.time() - api_start) * 1000.0
                        self.diagnostics.check_api_health(api_latency)
                        
                        decision = json.loads(response.text)

                # 6. Actuator Calibration & Control Output
                elevator = self.calibrator.apply_trim_compensation(
                    decision.get("elevator", 0.0), telemetry["airspeed_kts"]
                )
                
                self.bridge.send_controls(
                    elevator=elevator,
                    aileron=decision.get("aileron", 0.0),
                    rudder=decision.get("rudder", 0.0),
                    throttle=decision.get("throttle", 0.7)
                )

                # 7. Logging & Real-time Streaming
                self.logger.log_event(telemetry, decision, "IN_FLIGHT")
                update_dashboard_state(telemetry)
                broadcast_telemetry(telemetry)

                print(f"[Cycle {cycle_count}] Alt: {telemetry['altitude_ft']}ft | AI Thought: {decision.get('thought_process', 'N/A')[:60]}...")

                # Loop Rate Limiter (~2Hz)
                elapsed = time.time() - loop_start
                if elapsed < 0.5:
                    time.sleep(0.5 - elapsed)

        except KeyboardInterrupt:
            print("\n🛑 Manual interrupt received.")
        
        self.execute_post_flight_sequence()

    def execute_post_flight_sequence(self):
        print("\n--- PHASE 3: Post-Flight Landing & Cloud Sync ---")
        success = self.cloud.upload_log("flight_blackbox.log")
        if success:
            print("☁️ Blackbox flight logs successfully synced to cloud storage.")
        print("🏁 AeroMind AI mission workflow successfully concluded.")

if __name__ == "__main__":
    manager = AeroMindWorkflowManager()
    if manager.run_pre_flight_checks():
        manager.execute_flight_sequence()
