# 🔧 Installation Guide – Sintrones Edge AI Starter Kit

This project ships a **pre‑wired Streamlit dashboard** with **17 tabs** and a **SQLite** backbone.

## 1) Prerequisites
- Python 3.9+ (tested on 3.11)
- pip 21+
- macOS / Ubuntu / WSL2
- Optional: GPU runtimes (OpenVINO/TensorRT)
- Optional: MQTT broker (Mosquitto) for sidecar tests

## 2) Create a virtual environment
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip setuptools wheel
```

## 3) Install dependencies
```bash
pip install -r requirements.txt
```

## 4) Initialize SQLite (idempotent)
```bash
python scripts/init_sqlite.py
```
> Script is path‑robust (adds repo root to `sys.path`).

## 5) Run the dashboard
```bash
streamlit run app.py
```

## 6) Optional: Docker (dashboard + MQTT broker)
```bash
docker compose -f packaging/docker-compose.yml up --build
```

## 7) Optional: Mosquitto locally
macOS (brew)
```bash
brew install mosquitto && brew services start mosquitto
```
Ubuntu
```bash
sudo apt install -y mosquitto mosquitto-clients
```

---

### Notes / Common fixes
- Use explicit interpreter if activation fails:
  ```bash
  python3 -m venv .venv
  ./.venv/bin/python -m pip install --upgrade pip setuptools wheel
  ./.venv/bin/python -m pip install -r requirements.txt
  ./.venv/bin/python scripts/init_sqlite.py
  ./.venv/bin/python -m streamlit run app.py
  ```
- Ensure you run from **repo root** (same folder as `app.py`).

