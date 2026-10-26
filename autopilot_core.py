import time
import json
from google import genai
from google.genai import types
from earth_bridge import EarthFlightBridge
from prompts import SYSTEM_PROMPT

# Initialize Gemini Client (uses GEMINI_API_KEY environment variable)
client = genai.Client()
bridge = EarthFlightBridge()

def run_autopilot_loop():
    print("🚀 Unmanned Gemini Flight Driver Initialized...")
    
    while True:
        try:
            # 1. Pull live data from Earth/Sim bridge
            telemetry = bridge.get_telemetry()
            
            # 2. Formulate prompt payload
            user_prompt = f"Current Telemetry: {json.dumps(telemetry)}. Determine next structural control tweaks."
            
            # 3. Query Gemini 4 Argon for high-reasoning flight management
            response = client.models.generate_content(
                model='gemini-4-argon',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    response_mime_type="application/json",
                    temperature=0.2, # Low temperature for deterministic, safe flight control
                ),
            )
            
            # 4. Parse control outputs
            decision = json.loads(response.text)
            print(f"🤖 AI Thought: {decision.get('thought_process')}")
            
            # 5. Actuate controls back into simulation / flight mapper
            bridge.send_controls(
                elevator=decision.get("elevator", 0.0),
                aileron=decision.get("aileron", 0.0),
                rudder=decision.get("rudder", 0.0),
                throttle=decision.get("throttle", 0.7)
            )
            
            # Tick rate for control loop (e.g., 2Hz - 5Hz)
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print("\n🛑 Autopilot disengaged safely by user.")
            break
        except Exception as e:
            print(f"⚠️ Error in autopilot cycle: {e}")
            time.sleep(1.0)

if __name__ == "__main__":
    run_autopilot_loop()
