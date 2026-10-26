import json
import datetime

class BlackBoxLogger:
    def __init__(self, filename="flight_blackbox.log"):
        self.filename = filename

    def log_event(self, telemetry: dict, decision: dict, status: str):
        record = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "telemetry": telemetry,
            "ai_decision": decision,
            "flight_status": status
        }
        with open(self.filename, "a") as f:
            f.write(json.dumps(record) + "\n")
