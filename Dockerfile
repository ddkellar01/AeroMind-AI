# AeroMind-AI — default image (autopilot service)
# Docker Hub builds this file automatically when no other Dockerfile is named.
# Same build as Dockerfile.autopilot — kept in sync intentionally.
#
# Build:  docker build -t <DOCKERHUB_USERNAME>/aeromind-autopilot:latest .
# Run:    docker run --rm -e GEMINI_API_KEY=<your-key> <DOCKERHUB_USERNAME>/aeromind-autopilot:latest
FROM python:3.10-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencies first (layer cache)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Application code (flat repo layout — modules import each other by name)
COPY *.py ./

# Run as non-root
RUN useradd --create-home --uid 10001 aeromind \
    && chown -R aeromind:aeromind /app
USER aeromind

# autopilot_core.py builds genai.Client() at import time and fails fast
# without a key — pass it at run time, never bake it into the image:
#   docker run -e GEMINI_API_KEY=... <image>
CMD ["python", "autopilot_core.py"]
