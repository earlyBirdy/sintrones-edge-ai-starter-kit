
# 📦 Sintrones Edge AI Starter Kit

> **“Edge AI Vision + Sensor Gateway” for Vehicle / Factory / City Use**

This open-source project demonstrates how to deploy real-time AI object detection, sensor data fusion, and industrial dashboards using **Sintrones rugged Edge AI hardware**. It’s built for system integrators, developers, and researchers working in transportation, manufacturing, and smart infrastructure.

> 💡 **Sales + Collaboration**: Use this as a customer-facing PoC and R&D starter kit. Ideal for OEMs, system integrators, and smart infrastructure pilots in SEA or global deployments.

---

## 🚀 Features

- 📷 Use real camera + industrial sensor inputs (USB, PoE, RS232, etc.)
- 🧠 Deploy AI models like YOLOv5 or OpenVINO for object detection
- 📊 Display data and AI results via Streamlit or Grafana dashboard
- 🔌 Communicate via **MQTT**, **Modbus**, or **CANBus**
- 📡 Optional integration of **5G modules + GPS** for mobile/vehicular use
- 🔄 Built-in OTA update agent for field-deployed upgrades
- **AI Agents Add-on**:
  - ⚡ *System Recovery Agent* monitors MQTT heartbeats and triggers recovery actions.
  - 🔧 *Adapter Auto-Gen Agent* inspects MQTT/OPC UA and generates adapter configs.
  - 📦 *Release Agent* runs `tools/healthcheck.py` and drafts `dist/release_notes.md`.
- **Vision Inspection**: camera publisher sample and ONNX dummy model generator.
- **Healthcheck Tool**: `tools/healthcheck.py` to verify syntax, deps, and structure.

---

## 🤝 Sales + Technical Collaboration

This starter kit aligns with Sintrones’ efforts to:
- Support system integrators and OEMs with demo-ready tools
- Collaborate on R&D and proof-of-concepts
- Promote industrial AI adoption across SEA & global markets

Use it as a base to build your own PoC, integrate with Odoo IoT, or contribute modules!

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

## 📢 Community & Contact

- [Website](https://www.sintrones.com)
- [LinkedIn](https://www.linkedin.com/company/sintrones-technology-corp/posts/?feedView=all)
- [Edge AI Community (Coming soon)](#)

📬 Want a hardware demo kit? [Contact Sintrones](https://www.sintrones.com/contact/)

---

## 📄 License

MIT License — open for research, testing, and pilot deployment.
