# 🔧 Installation Guide – Sintrones Edge AI Starter Kit

This guide walks you through setting up your environment and running the Sintrones Edge AI Starter Kit. This project ships a **pre‑wired Streamlit dashboard** for an Edge AI Vision Inspection starter kit with **17 tabs**. It includes Model Packs, Fleet, Benchmark Matrix, Data Traceability, Triage → Rules, Yield & Quality, Pipeline Builder,
I/O Connectors, Governance, and more.

## 1. System Requirements

- Python 3.8 or newer
- pip 21+
- OS: Ubuntu 20.04+, macOS, or Windows WSL2
- Optional: GPU (for ONNX/OpenVINO inference)
- MQTT broker (e.g., Mosquitto for local test)
- (Optional) Git, DVC, Git‑LFS for data governance

## 2. Clone the Repository

```bash
git clone https://github.com/earlyBirdy/sintrones-edge-ai-starter-kit.git
cd sintrones-edge-ai-starter-kit
```

## 3. Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install --upgrade pip
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

> Contains all core, vision, and dashboard dependencies

## 5. Launch the Dashboard

```bash
streamlit run app.py

```

> All functionality is integrated inside the unified dashboard: fine-tuning, benchmarking, explainability, and more.

## 6. MQTT (Optional)

**macOS**
```bash
brew install mosquitto
brew services start mosquitto
```

**Ubuntu**
```bash
sudo apt install mosquitto mosquitto-clients
```

**Docker**
```bash
docker run -it -p 1883:1883 eclipse-mosquitto
```

✅ You're now running the fully integrated Edge AI dashboard!
