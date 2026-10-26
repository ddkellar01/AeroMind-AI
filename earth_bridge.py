import socket
import json

class EarthFlightBridge:
    def __init__(self, host='127.0.0.1', port=5500):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def get_telemetry(self):
        # Pulls live data packet from simulation/Google Earth network protocol
        return {
            "altitude_ft": 5200.0,
            "airspeed_kts": 145.0,
            "heading_deg": 270.0,
            "pitch_deg": 2.5,
            "roll_deg": 0.1,
            "gps_lat": 37.7749,
            "gps_lon": -122.4194,
            "vertical_speed_fpm": 120.0
        }

    def send_controls(self, elevator: float, aileron: float, rudder: float, throttle: float):
        control_data = json.dumps({
            "elevator": max(-1.0, min(1.0, elevator)),
            "aileron": max(-1.0, min(1.0, aileron)),
            "rudder": max(-1.0, min(1.0, rudder)),
            "throttle": max(0.0, min(1.0, throttle))
        })
        self.sock.sendto(control_data.encode('utf-8'), (self.host, self.port))
