# AeroMind-AI — full workflow service (workflows.py)
# AeroMindWorkflowManager: pre-flight checks -> autonomous flight loop ->
# post-flight cloud sync. Starts the dashboard on 8080 in a background thread.
#
# REQUIRES the 7 companion modules shipped in this bundle (they are missing
# from the repo today and workflows.py cannot import without them):
#   vision_mapper.py, collision_avoidance.py, emergency_handler.py,
#   system_diagnostics.py, actuator_calibrator.py, cloud_sync.py,
#   telemetry_streamer.py
#
# Build:  docker build -f Dockerfile.workflow -t <DOCKERHUB_USERNAME>/aeromind-workflow:latest .
# Run:    docker run --rm -p 8080:8080 -e GEMINI_API_KEY=<your-key> <DOCKERHUB_USERNAME>/aeromind-workflow:latest
FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

# Blackbox log lives in /app — give the non-root user a writable data dir
RUN useradd --create-home --uid 10001 aeromind \
    && mkdir -p /app/data \
    && chown -R aeromind:aeromind /app
USER aeromind

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/api/status', timeout=4)" || exit 1

CMD ["python", "workflows.py"]
