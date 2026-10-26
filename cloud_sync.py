"""SystemDiagnostics — API / loop health tracking for workflows.py.

workflows.py calls diagnostics.check_api_health(latency_ms) once per
flight cycle. Tracks rolling latency and flags a degraded link when
the average exceeds the threshold.
"""


class SystemDiagnostics:
    def __init__(self, latency_threshold_ms: float = 5000.0, window: int = 20):
        self.latency_threshold_ms = latency_threshold_ms
        self.window = window
        self.latency_samples: list[float] = []
        self.api_healthy = True

    def check_api_health(self, latency_ms: float) -> bool:
        self.latency_samples.append(latency_ms)
        if len(self.latency_samples) > self.window:
            self.latency_samples.pop(0)
        avg = sum(self.latency_samples) / len(self.latency_samples)
        self.api_healthy = avg <= self.latency_threshold_ms
        if not self.api_healthy:
            print(f"⚠️ Diagnostics: Gemini API latency degraded (avg {avg:.0f} ms)")
        return self.api_healthy
