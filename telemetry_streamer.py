"""TelemetryStreamer — live telemetry broadcast for workflows.py.

workflows.py calls:
    start_streamer_thread()          once, before the flight loop
    broadcast_telemetry(telemetry)   once per cycle
Holds the latest telemetry snapshot in a thread-safe slot that the
dashboard (or a future websocket layer) can read. No sockets are
opened here, so it is safe in any container.
"""

import threading

_latest_telemetry: dict = {}
_lock = threading.Lock()
_thread: threading.Thread | None = None


def _streamer_loop():
    # Placeholder loop: the streamer thread owns periodic fan-out.
    # broadcast_telemetry() writes the shared slot synchronously, so the
    # loop only needs to stay alive as a daemon alongside the workflow.
    threading.Event().wait()


def start_streamer_thread():
    global _thread
    if _thread is not None and _thread.is_alive():
        return _thread
    _thread = threading.Thread(target=_streamer_loop, daemon=True, name="telemetry-streamer")
    _thread.start()
    return _thread


def broadcast_telemetry(telemetry: dict):
    with _lock:
        _latest_telemetry.clear()
        _latest_telemetry.update(telemetry)


def get_latest_telemetry() -> dict:
    with _lock:
        return dict(_latest_telemetry)
