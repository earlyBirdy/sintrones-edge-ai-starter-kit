# 📦 Sintrones Edge AI Starter Kit

> **“Edge AI Vision + Sensor Gateway” for Vehicle / Factory / City Use**

This open-source project demonstrates how to deploy real-time AI object detection, sensor data fusion, and industrial dashboards using **Sintrones rugged edge AI hardware**. It’s built for system integrators, developers, and researchers working in transportation, manufacturing, and smart infrastructure.

---

## 🚀 Features

- 📷 Use real camera + industrial sensor inputs (USB, PoE, RS232, etc.)
- 🧠 Deploy AI models like YOLOv5 or OpenVINO for object detection
- 📊 Display data and AI results via Streamlit or Grafana dashboard
- 🔌 Communicate via **MQTT**, **Modbus**, or **CANBus**
- 📡 Optional integration of **5G modules + GPS** for mobile/vehicular use
- 🔄 Built-in OTA update agent for field-deployed upgrades

---

## 🛠️ Project Structure

```
sintrones-edge-ai-starter-kit/
├── ai_models/             # YOLOv5 or OpenVINO model files
├── sensor_drivers/        # CANbus, Modbus, GPIO, MQTT handlers
├── dashboard/             # Streamlit and Grafana dashboard configs
├── docker/                # Dockerfile + docker-compose.yml
├── app/                   # Core application logic
│   └── main.py
├── ota/                   # OTA update agent and JSON control
├── configs/               # System & sensor configuration files
├── examples/              # Application-specific integration (vehicle, factory, city)
├── docs/                  # Wiring diagrams, ABOX-5220 architecture
│   └── index.md
├── LICENSE
├── README.md
├── INSTALL.md
├── requirements.txt
├── .gitignore
```

---


## 📦 Deployment Options

| Mode             | Description                                  |
|------------------|----------------------------------------------|
| **Standalone**   | Fully offline dashboard & sensor integration |
| **Edge-to-Cloud**| MQTT to Odoo, AWS, or other IoT platforms     |
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

## 🤝 Sales + Technical Collaboration

This starter kit aligns with Sintrones’ efforts to:
- Support system integrators and OEMs with demo-ready tools
- Collaborate on R&D and proof-of-concepts
- Promote industrial AI adoption across SEA & global markets

Use it as a base to build your own PoC, integrate with Odoo IoT, or contribute modules!

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

### 4) MQTT topics (default)
- `factory/vision/detections` – raw detections (per frame)
- `factory/vision/events` – filtered/decided events (if you wire through decision engine)

### 5) Troubleshooting
- **Model not found**: ensure `models/defect_detector.onnx` exists or pass an absolute path with `--model`.
- **Unsupported IR version**: upgrade `onnxruntime` or re-generate model with IR=10.
- **No camera**: use `--video` with a test clip.
- **Broker connection**: start Mosquitto locally or point to your broker in `examples/vision_inspection/camera_infer.py` (MQTT_HOST/PORT).

---

## 📢 Community & Contact

- [Website](https://www.sintrones.com)
- [LinkedIn](https://www.linkedin.com/company/sintrones-technology-corp/posts/?feedView=all)
- [Edge AI Community (Coming soon)](#)

📬 Want a hardware demo kit? [Contact Sintrones](https://www.sintrones.com/contact/)

---

## 📄 License

MIT License — open for research, testing, and pilot deployment.
