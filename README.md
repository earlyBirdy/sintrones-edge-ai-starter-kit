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

## 📢 Community & Contact

- [Website](https://www.sintrones.com)
- [LinkedIn](https://www.linkedin.com/company/sintrones-technology-corp/posts/?feedView=all)
- [Edge AI Community (Coming soon)](#)

📬 Want a hardware demo kit? [Contact Sintrones](https://www.sintrones.com/contact/)

---

## 📄 License

MIT License — open for research, testing, and pilot deployment.



