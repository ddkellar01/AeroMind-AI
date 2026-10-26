![AeroMind AI](1793053730449.jpg)

# AeroMind-AI

[![AeroMind AI CI/CD & Simulation Pipeline](https://github.com/ddkellar01/AeroMind-AI/actions/workflows/autopilot.yml/badge.svg)](https://github.com/ddkellar01/AeroMind-AI/actions/workflows/autopilot.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Model](https://img.shields.io/badge/Model-Gemini%204%20Argon-orange.svg)](https://deepmind.google/technologies/gemini/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Embedded%20%7C%20Simulation-lightgrey.svg)](#platform-support--hardware-architecture)

---

## What is this?

AeroMind AI is an unmanned, zero-crew autonomous flight driver leveraging Gemini high-reasoning models and real-time Google Earth telemetry. It computes advanced trajectory adjustments, manages multi-axis flight stability, and executes precision steering loops entirely independent of human pilots or flight attendants.

---

## 🧰 Tech Stack Badges & Architecture

| Category | Technologies |
| :--- | :--- |
| **Workflow Status** | [![AeroMind AI CI/CD & Simulation Pipeline](https://github.com/ddkellar01/AeroMind-AI/actions/workflows/autopilot.yml/badge.svg)](https://github.com/ddkellar01/AeroMind-AI/actions/workflows/autopilot.yml) |
| **Core AI Model** | [![Gemini 4 Argon](https://img.shields.io/badge/Gemini-4%20Argon-8E44AD?logo=google&logoColor=white)](https://ai.google.dev/) |
| **Language & Runtime** | [![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)](https://www.python.org/) |
| **Web Framework & Sockets** | [![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/) [![Flask-Sock](https://img.shields.io/badge/Flask--Sock-0.7.0-blue)](https://pypi.org/project/flask-sock/) |
| **Data Validation & Math** | [![Pydantic](https://img.shields.io/badge/Pydantic-2.0-E92063?logo=pydantic&logoColor=white)](https://docs.pydantic.io/) [![NumPy](https://img.shields.io/badge/NumPy-1.24.0-013243?logo=numpy&logoColor=white)](https://numpy.org/) |
| **Testing & Linting** | [![Pytest](https://img.shields.io/badge/Pytest-8.0-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/) [![Flake8](https://img.shields.io/badge/Flake8-Linter-4B8BBE)](https://flake8.pycqa.org/) |

### 💻 Core Programming Languages & Core Systems
* **Python 3.10+**: Core execution environment, autonomous decision loops, sensor fusion algorithms, and HTTP/WebSocket dashboard servers.
* **Google Gemini SDK (`google-genai`)**: High-reasoning structured decision engine (`gemini-4-argon`) enforcing precise JSON flight control parameters.

### ⛓️ Web3 & Infrastructure
* **Distributed Network Socket Protocols**: Custom UDP telemetry bridge interface for real-time synchronization with Google Earth flight simulation protocols.
* **Cloud Telemetry Synchronization**: Blackbox logger with encrypted cloud sync pipelines for post-flight audit logging.

### ⚙️ Platform Support & Hardware Architecture
* **Cross-Platform Support**: Tested on Linux (`ubuntu-latest`), embedded x86_64 systems, and flight simulator ground stations.
* **UDP Communication Interface**: Socket interface supporting standard UDP payload ingestion (`AF_INET`, `SOCK_DGRAM`) on low-latency local interfaces.

### ⚡ Low-Level Infrastructure & Performance
* **Sensor Fusion Engine**: Low-pass filter smoothing algorithms with pitch and G-force complementary filtering to eliminate telemetry jitter.
* **Hardcoded Safety Overrides**: Real-time safety envelope monitor verifying altitude bounds, stall speeds, and maximum G-forces with sub-millisecond override intervention.
* **Deterministic Flight Actuation**: Closed-loop control system operating at 2Hz–5Hz control ticks with deterministic temperature controls (`temperature=0.2`).

### 🛠️ DevOps & Build Tools
* **GitHub Actions**: Automated CI/CD pipeline (`autopilot.yml`) executing linting, dependency verification, and simulation harness tests on push/pull requests.
* **Flake8**: Static code analysis enforcing strict syntax and code style compliance.
* **Pytest**: Automated regression testing and flight simulation edge-case verification.

### ☁️ Cloud
* **Google Gemini Cloud API**: High-throughput reasoning API for automated waypoint navigation and meteorological adaptation.
* **Cloud Log Storage**: Automated blackbox log uploading for post-mission telemetry analytics.

---

## 🏛️ What Is This About?

### What this does
1. **Telemetry Ingestion**: Ingests real-time flight telemetry (altitude, airspeed, heading, pitch, roll, G-force, GPS coordinates, and vertical speed) over a UDP socket bridge from Google Earth or simulator feeds.
2. **Sensor Processing**: Applies noise reduction and complementary smoothing across raw telemetry signals via `sensor_fusion.py`.
3. **Reasoning & Flight Correction**: Streams sensor fusion payloads and waypoint navigation markers into **Gemini 4 Argon**, receiving structured JSON flight control parameters (elevator, aileron, rudder, and throttle adjustments).
4. **Safety Envelope Enforcement**: Checks all maneuvers against safety limits in `safety_monitor.py`. Overrides controls automatically if stall warnings, terrain proximity, or excessive G-forces are detected.
5. **Real-time Dashboard & Blackbox**: Exposes live telemetry and control loop telemetry via a Flask HTTP/WebSocket dashboard and records immutable flight logs locally and to cloud storage.

### Why is this cool?
* **Zero-Crew Autonomous Control**: Replaces traditional human autopilot rules with a high-reasoning multimodal LLM capable of understanding contextual flight conditions.
* **Deterministic Safety Layer**: Combines non-deterministic neural reasoning with deterministic mathematical safety bounds to guarantee flight envelope compliance.
* **Edge Simulation Injector**: Includes a simulation harness capable of injecting severe edge cases (microbursts, sensor dropouts) on the fly to test agent recovery strategies.

### What problems this solves
* **Human Error Elimination**: Prevents pilot fatigue and loss-of-control scenarios during complex navigational procedures or adverse weather.
* **Sensor Noise Instability**: Smooths raw flight telemetry jitter before feeding inputs to autonomous decision controllers.
* **Unpredictable AI Behavior**: Guarantees deterministic output parsing via strict JSON schemas and instant hardcoded safety overrules.

---

## How to install this?

### Requirements
* **Python**: `3.10` or higher
* **Google Gemini API Key**: `GEMINI_API_KEY` set in your environment variables
* **OS**: Linux, macOS, or Windows WSL2

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/ddkellar01/AeroMind-AI.git](https://github.com/ddkellar01/AeroMind-AI.git)
   cd AeroMind-AI
