from flask import Flask, jsonify
import threading

app = Flask("AeroMind-Dashboard")
latest_telemetry = {}

@app.route("/api/status")
def get_status():
    return jsonify(latest_telemetry)

def update_dashboard_state(data: dict):
    global latest_telemetry
    latest_telemetry = data

def run_dashboard_server():
    app.run(host="0.0.0.0", port=8080, debug=False, use_reloader=False)

def start_dashboard_background():
    t = threading.Thread(target=run_dashboard_server, daemon=True)
    t.start()
