# 🔧 Installation Guide – Sintrones Edge AI Starter Kit

This guide walks you through setting up your environment and running the Sintrones Edge AI Starter Kit.

## 1️⃣ System Requirements

- Python 3.8 or newer
- pip 21+
- OS: Ubuntu 20.04+, macOS, or Windows WSL2
- Optional: GPU (for ONNX/OpenVINO inference)
- MQTT broker (e.g., Mosquitto for local test)

## 2️⃣ Clone the Repository

```bash
git clone https://github.com/earlyBirdy/sintrones-edge-ai-starter-kit.git
cd sintrones-edge-ai-starter-kit
```

## 3️⃣ Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

_For AI Agents:_
```bash
pip install -r requirements-addon.txt
```

## 4️⃣ Run Dashboard Demo

```bash
python app/main.py
```

## 5️⃣ Launch Streamlit Log Viewer (Optional)

```bash
streamlit run dashboard/log_viewer.py
```

## 6️⃣ Optional MQTT Broker (Mosquitto)

**macOS:**
```bash
brew install mosquitto
brew services start mosquitto
```

**Ubuntu:**
```bash
sudo apt install mosquitto mosquitto-clients
mosquitto -v
```

**Docker:**
```bash
docker run -it -p 1883:1883 eclipse-mosquitto
```

## ✅ You're ready!

Check out the `/examples` folder to test visual inspection flows.
## 🛠️ New Modules & Setup

To use the enhanced features:

```bash
pip install -r requirements.txt
```

### Optional Installs
- For Streamlit UI: `pip install streamlit`
- For MQTT sync: `pip install paho-mqtt`
- For benchmarking (ONNX runtime/tensorrt): follow hardware-specific docs

### Start Fine-Tuning UI
```bash
streamlit run dashboard/fine_tune_ui.py
```

### Start Benchmark Panel
```bash
streamlit run dashboard/benchmark_panel.py
```

### Run Health Check
```bash
python tools/health_check.py
```

---
