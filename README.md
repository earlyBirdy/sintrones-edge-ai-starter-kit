
# 📦 Sintrones Edge AI Starter Kit
![Test Status](https://github.com/earlyBirdy/sintrones-edge-ai-starter-kit/actions/workflows/python-ci.yml/badge.svg)

> **“Edge AI Vision + Sensor Gateway” for Vehicle / Factory / City Use**

The Sintrones Edge AI Starter Kit is a production-ready, open-source framework designed to accelerate **real-world deployments** of AI-enhanced sensor fusion across vehicles, factories, and smart cities.

Built on rugged industrial-grade hardware, it enables seamless integration of **vision AI**, **sensor telemetry**, **edge dashboards**, and **protocol adapters** (MQTT, Modbus, CANbus) to create deployable proof-of-concepts and real-time systems.

Ideal for **system integrators**, **smart factory teams**, and **urban solution architects**, this repo provides all core modules and examples to quickly demonstrate AI value at the edge.

> 💡 **Sales + Collaboration**: Use this as a customer-facing PoC and R&D starter kit. Ideal for OEMs, system integrators, and smart infrastructure pilots in Thailand or SEA deployments.

---

## 🚀 Features

- 🎥 **Multi-Modal Sensor Input** — Real camera streams + industrial signals (USB, PoE, RS232, GPIO)
- 🧠 **AI Model Inference** — Supports YOLOv5, OpenVINO, or ONNX for object detection and event logic
- 📊 **Dashboards** — Visualize detections and sensor states via Streamlit (lightweight) or Grafana (pro)
- 🔌 **Industrial Protocol Support** — Communicates via MQTT, Modbus RTU/TCP, and CANBus for machine/vehicle data
- 📡 **Mobility-Ready** — Integrates 5G modules, GNSS/GPS, and CAN for use in transportation/fleet systems
- 🔄 **OTA Management** — Update devices in the field via JSON-controlled OTA agent
- 🤖 **AI Agent Framework** — Add-on agents include:
  - ⚡ *System Recovery Agent* for fault detection and recovery
  - 🔧 *Adapter Auto-Gen Agent* to auto-generate configs for new devices (MQTT/OPC-UA)
  - 📦 *Release Agent* to run readiness tests and publish release notes
- 🧪 **Vision Inspection Demos** — ONNX model generator + camera inferencing pipeline
- 🔍 **Repo Healthcheck** — Lint and structure audit via `tools/healthcheck.py`

---

## 🤝 Sales + Technical Collaboration

This starter kit aligns with Sintrones’ efforts to:
- 🛠️ Support System Integrators and SMEs with demo-ready tools
- 🤝 Collaborate on R&D and Proof-of-Concepts
- 🌏 Promote industrial AI adoption across Thailand & SEA markets

Use it as a base to build your own PoC, integrate with IIoT, or contribute modules! this repo helps you **accelerate time-to-demo and validate value** at the edge.

---

## 🆓 vs 💼 Commercial Version

| Feature                                | Open-Source Starter Kit | Commercial Offering |
|----------------------------------------|--------------------------|---------------------|
| Real-time AI Inference (YOLO, etc.)    | ✅ Yes                   | ✅ Yes              |
| Dashboard UI (Streamlit/Grafana)       | ✅ Yes                   | ✅ Yes              |
| OTA Agent                              | ✅ Yes                   | ✅ Enhanced         |
| Health Monitoring                      | ✅ CLI Tool              | ✅ Web Dashboard    |
| AI Agent Automation (Recovery, Adapter)| ✅ Yes                   | ✅ Advanced         |
| Odoo / Cloud / AWS Integration         | 🟡 Manual                | ✅ Plug-in Ready    |
| Hardware Acceleration Support          | 🟡 Generic               | ✅ Tuned Drivers    |
| Long-term Support + SLA                | ❌                       | ✅ Yes              |
| Turnkey Packaging (VM/Image)           | ❌                       | ✅ Yes              |

---

## 📦 Deployment Options

| Mode             | Description                                  |
|------------------|----------------------------------------------|
| **Standalone**   | Fully offline dashboard & sensor integration |
| **Edge-to-Cloud**| MQTT to Odoo, AWS, or other IoT platforms    |
| **Vehicle AI**   | Add GPS/CANbus for on-road deployments       |

---

## 🎯 Use Cases

- 📦 **Smart Logistics** – Detect vehicles or goods, monitor temperature/vibration
- 🏭 **Factory Automation** – Visual inspection + machine health monitoring
- 🏙️ **Smart Cities** – Public space detection, traffic analytics, air quality

---

## 📚 Additional Resources

- 📘 [Use Cases](/docs/USE_CASES.md): Real-world Edge AI applications in factories, vehicles, and smart cities  
- 🤝 [Contributing Guide](/docs/CONTRIBUTING.md): How to get involved and contribute to this project

---

## AI Agents Add-on

This repository integrates an **AI Agents Add-on** with three useful agents to enhance reliability, adaptability, and release workflows.

### 1. System Recovery Agent
- **Purpose**: Monitors MQTT heartbeat topics (e.g., `factory/health/#`).
- **Behavior**: If a device misses heartbeats for a configured timeout, it triggers recovery actions (e.g., restart services or notify operators).
- **Usage**:
  ```bash
  python -m src.agents.system_recovery_agent --config agents/system_recovery.yaml
  ```

### 2. Adapter Auto-Gen Agent
- **Purpose**: Inspects new devices and automatically generates adapter configuration snippets.
- **Modes**:
  - **MQTT sniff mode**: listens to wildcard topics and infers field mappings.
  - **OPC UA browse mode**: enumerates nodeIds and proposes mappings.
- **Usage**:
  ```bash
  # MQTT mode
  python -m src.agents.adapter_autogen_agent --mode mqtt --host localhost --topic factory/# --samples 30 --timeout 20

  # OPC UA mode
  python -m src.agents.adapter_autogen_agent --mode opcua --endpoint opc.tcp://192.168.10.20:4840
  ```

### 3. Release Agent
- **Purpose**: Automates readiness checks and drafts GitHub release notes.
- **Behavior**: Runs `tools/healthcheck.py`, verifies syntax & dependencies, and generates release notes into `dist/release_notes.md`.
- **Usage**:
  ```bash
  python -m src.agents.release_agent --tag v0.3.0 --notes "Adapters + Vision QA"
  ```

### 4) MQTT topics (default)
  - `factory/vision/detections` – raw detections (per frame)
  - `factory/vision/events` – filtered/decided events (if you wire through decision engine)

### 5) Troubleshooting
  - **Model not found**: ensure `models/defect_detector.onnx` exists or pass an absolute path with `--model`.
  - **Unsupported IR version**: upgrade `onnxruntime` or re-generate model with IR=10.
  - **No camera**: use `--video` with a test clip.
  - **Broker connection**: start Mosquitto locally or point to your broker in `examples/vision_inspection/camera_infer.py` (MQTT_HOST/PORT).

### Requirements
Install additional dependencies with:
```bash
python -m pip install -r requirements-addon.txt
```

### Outputs
- **Recovery logs**: console output
- **Auto-generated configs**: `dist/config.autogen.yaml`
- **Release notes**: `dist/release_notes.md`

For more details, see [`docs/AGENTS.md`](docs/AGENTS.md).

---

## 🛠️ Project Structure

```
sintrones-edge-ai-starter-kit/
├─- agents/                # Agent configs (e.g., system_recovery.yaml)
├── ai_models/             # YOLOv5 or OpenVINO model files
├── app/                   # Core dashboard + logic
│   └── main.py
├── configs/               # System & sensor configuration files
│   └─ config.yaml
├── dashboard/             # Streamlit and Grafana dashboard configs
├─- dist/                  # Auto-generated configs and release notes
├── docker/                # Dockerfile + docker-compose.yml
├── docs/                  # Wiring diagrams, ABOX-5220 architecture
│   └── index.md
│   └─ AGENTS.md           # Documentation for AI Agents
├── examples/              # Application-specific integration (vehicle, factory, city)
│   └─ vision_inspection/...
├─- models/
│   └─ defect_detector.onnx
├── ota/                   # OTA update agent and JSON control
├── sensor_drivers/        # CANbus, Modbus, GPIO, MQTT handlers
├─- src/
│   ├─ agents/             # AI Agents (system recovery, adapter autogen, release agent)
│   ├─ collector.py
│   ├─ batcher.py
│   ├─ cli.py
│   └─ decision_engine/
│      └─ engine.py
├─- tools/
│   └─ healthcheck.py       # Repo healthcheck tool
├─- requirements.txt
├─- requirements-addon.txt  # Dependencies for AI Agents
├── INSTALL.md
├── README.md
├── LICENSE
├── .gitignore
```

---

## ⚡ Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sintrones/edge-ai-starter-kit.git
   cd edge-ai-starter-kit
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard demo:**
   ```bash
   python app/main.py
   ```

## Vision Inspection Camera Publisher

This example publishes **per-frame detections** to MQTT for the collector to ingest. It supports a real ONNX model or a mock fallback.

### 1) Install dependencies
```bash
# Core
python -m pip install onnxruntime opencv-python paho-mqtt

# Apple Silicon (M1/M2/M3): use the silicon wheel
# python -m pip install onnxruntime-silicon opencv-python paho-mqtt
```

### 2) Prepare a model (optional)
If you already have an ONNX model (e.g., YOLO export), put it in `models/defect_detector.onnx`.

Otherwise, generate a tiny test model (always outputs one detection):
```bash
python models/onnx-model-generator/generate_dummy_onnx_with_onnx.py
# -> writes models/defect_detector.onnx
```

> **Note:** If you see an error like *Unsupported model IR version: 11, max supported IR version: 10*, either upgrade onnxruntime (`pip install --upgrade onnxruntime` or `onnxruntime-silicon`) or regenerate the model with IR=10.

### 3) Run the camera publisher
Use a webcam:
```bash
python examples/vision_inspection/camera_infer.py \
  --model models/defect_detector.onnx --camera 0
```
Or a sample video:
```bash
python examples/vision_inspection/camera_infer.py \
  --model models/defect_detector.onnx --video path/to/sample.mp4
```

If you don’t have a model yet, run the mock-fallback script (publishes synthetic detections periodically):
```bash
python onnx-model-generator-ready/camera_infer_mock_fallback.py --camera 0
# or
python onnx-model-generator-ready/camera_infer_mock_fallback.py --video path/to/sample.mp4
```

```bash
# Collector should already be running to write JSONL
python -m src.cli collect --config configs/config.yaml

# Batch to Parquet
python -m src.cli batch --config configs/config.yaml
```

---

## 🧠 ONNX Model Troubleshooting

If you encounter errors like:

> `Unsupported model IR version: 11, max supported IR version: 10`

You can either:

1. Upgrade your ONNX runtime:
   ```bash
   pip install --upgrade onnxruntime
   ```

2. Re-export the model with `ir_version=10`

---

### ⚡🔧📦 AI Agents Quick-Start

- ⚡ **System Recovery Agent**  
  ```bash
  python -m src.agents.system_recovery_agent --config agents/system_recovery.yaml
  ```

- 🔧 **Adapter Auto-Gen Agent**  
  ```bash
  # MQTT mode
  python -m src.agents.adapter_autogen_agent --mode mqtt --host localhost --topic factory/# --samples 30 --timeout 20

  # OPC UA mode
  python -m src.agents.adapter_autogen_agent --mode opcua --endpoint opc.tcp://192.168.10.20:4840
  ```

- 📦 **Release Agent**  
  ```bash
  python -m src.agents.release_agent --tag v0.3.0 --notes "Adapters + Vision QA"
  ```

  > Install add-on dependencies:
  ```bash
  pip install -r requirements-addon.txt
  ```

  > Outputs include:
  - `dist/config.autogen.yaml`
  - `dist/release_notes.md`

  ---

### MQTT Broker (Mosquitto) — Quick Run

  Run locally:
  ```bash
  # macOS (brew)
  brew install mosquitto
  brew services start mosquitto

  # Ubuntu/Debian
  sudo apt update && sudo apt install -y mosquitto mosquitto-clients
  mosquitto -v  # foreground mode with verbose logs
  ```

  Or via Docker:
  ```bash
  docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
  ```

  Test:
  ```bash
  mosquitto_sub -h localhost -t "test/topic"
  mosquitto_pub -h localhost -t "test/topic" -m "hello"
  ```

---

## 🔍 Enhanced Vision Features (v1.1.0 Patch)

This patch includes additional AI/vision inspection modules for anomaly detection, logging, and RCA.

### ✅ New Capabilities

| Feature           | Module                           | Description |
|------------------|----------------------------------|-------------|
| Anomaly Detection| `anomaly/padim_infer.py`         | Basic visual anomaly scoring (extendable to PaDiM, DRAEM) |
| Frame Logger     | `logger/frame_logger.py`         | Save inspection snapshots with metadata |
| Root Cause Analysis (RCA) | `clustering/image_cluster.py` | Cluster visually similar defects using PCA + k-means |
| OTA Model Switch | `ota/model_switcher.py` + `update_control.json` | Swap ONNX models by version or line config |

### 🔧 Usage Examples

**Log a Frame and Metadata**
```python
from logger.frame_logger import save_frame_with_metadata
save_frame_with_metadata(image, {"line": "A1", "status": "PASS"})
```

**Run Anomaly Detection**
```python
from anomaly.padim_infer import detect_anomalies
result = detect_anomalies(image)
print(result["is_anomaly"], result["anomaly_score"])
```

**Switch Model via OTA Config**
```python
from ota.model_switcher import get_model_path_from_ota
model_path = get_model_path_from_ota()  # uses ota/update_control.json
```

**Cluster Image Features (RCA)**
```python
from clustering.image_cluster import cluster_features
labels = cluster_features(feature_array, n_clusters=4)
```

> These modules are designed to be extendable and can be linked with camera inference pipelines, OTA update agents, or retraining workflows.

---

## 🖥️ Streamlit Log Viewer

Use the built-in dashboard to browse visual inspection logs.

### ▶️ Launch Viewer
```bash
streamlit run dashboard/log_viewer.py
```

### 🔍 What It Does
- Displays image logs from `logs/*.jpg`
- Shows associated metadata from `logs/*.json`
- Sidebar shows count of PASS/FAIL units

---

## 🧪 Running Tests

Run all tests using:

```bash
pytest tests/
```

Tests include:
- Logger: saves annotated frame + JSON
- OTA model switch: reads ONNX path from control JSON

---

## 📢 Community & Contact

- [Website](https://www.sintrones.com)
- [LinkedIn](https://www.linkedin.com/company/sintrones-technology-corp/posts/?feedView=all)
- [Edge AI Community (Coming soon)](#)

📬 Want a hardware demo kit? [Contact Sintrones](https://www.sintrones.com/contact/)

---

## 📄 License

MIT License — open for research, testing, and pilot deployment.
