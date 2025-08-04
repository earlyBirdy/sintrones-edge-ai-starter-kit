# 🚀 Sintrones Edge AI Starter Kit

Welcome to the **Sintrones Edge AI Vision + Sensor Gateway**, an open-source kit built to showcase real-world applications using ruggedized hardware and AI-powered sensor monitoring.

## 🔧 Key Features

- 🧠 Edge AI Inference (YOLO/OpenVINO-ready)
- 📡 Sensor Gateway (Modbus, MQTT, CAN)
- 📈 Streamlit Dashboard Interface
- 🚚 Vehicle, Factory, Smart City Use Cases
- 🔁 OTA Update Logic for Field Deployment
- 🌍 Built for Developer Co-creation and Integration

## 🧰 Architecture

> *[Insert system diagram or wiring illustration here]*  
> *(Upload diagram.png to docs/ folder and uncomment below)*

<!-- ![System Architecture](diagram.png) -->

## 📦 Folder Overview

```plaintext
├── src/               # Main entry, edge inference logic
├── dashboard/         # Streamlit factory UI
├── examples/          # Use case demos (factory, vehicle, city)
├── ai_models/         # Placeholder for OpenVINO/YOLO models
├── sensor_drivers/    # Simulated sensor adapters
├── ota/               # OTA update simulation
├── docs/              # Wiring diagrams, setup instructions
```

## ⚙️ Quick Start

```bash
git clone https://github.com/earlyBirdy/sintrones-edge-ai-starter-kit.git
cd sintrones-edge-ai-starter-kit
pip install -r requirements.txt
python src/main.py
```

Or launch the dashboard:

```bash
streamlit run dashboard/app_factory.py
```

## 🧪 Sample Use Cases

- ✅ Factory Automation
- 🚚 Fleet Vibration + GPS Logging
- 🏙️ Smart City Environment Monitoring

## 📬 Contributions

We welcome system integrators, makers, and researchers to build on top of this. Start by forking the repo and checking `/examples/`.

## 📄 License

MIT License © 2025 Sintrones
