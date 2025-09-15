# 📦 Sintrones Edge AI Starter Kit
![Test Status](https://github.com/earlyBirdy/sintrones-edge-ai-starter-kit/actions/workflows/python-ci.yml/badge.svg)

**Edge AI Vision Inspection + Industrial IoT Sensor Gateway (Vehicle / Factory / City)**

A production‑minded, open framework to build **Edge AI** systems that combine **vision inspection**, **sensor telemetry**, and **industrial I/O** on rugged hardware. It ships a **Streamlit dashboard** (17 tabs), a **SQLite backbone**, **Model Packs**, **Fleet**, and a **Benchmark Matrix** to accelerate PoCs → pilots → deployments.

> Vision Inspection is **one of several Edge AI applications** supported by this kit. Use it as a customer‑facing PoC and R&D starter for OEMs, system integrators, and smart‑infrastructure pilots.

---

## ✅ What’s New (Sept 2025)
- **SQLite backbone** for on‑device metadata (devices, deployments, inspections, benchmarks, events, lineage)
- **SQL‑backed tabs**: **📇 Data Traceability**, **📈 Yield & Quality**, **🛰️ Fleet**
- **Model Packs** with validate/smoke‑test hooks + policies for **staged / shadow / rollback**
- **Benchmark Matrix gating** → auto‑select best engine (ONNX Runtime / OpenVINO / TensorRT) by **accuracy** & **latency**
- **ROC assist + A/B** helpers for setting inspection thresholds
- **Triage queue** enrichment (assignee & SLA) via structured events
- **Gateway sidecar (stub)** for MQTT→MES/Cloud and CDC table for safe sync
- **Plugin API** so integrators can add custom pre/post/rule steps
- **Dockerfile + docker‑compose** and a CI scaffold.

---

## 🤝 Sales + Technical Collaboration
- 🛠️ Support System Integrators and SMEs with demo‑ready tools
- 🤝 Collaborate on R&D and Proof‑of‑Concepts
- 🌏 Promote industrial AI adoption across Thailand & SEA markets

Use it as a base to build your own PoC, integrate with IIoT, or contribute modules — the repo helps you **accelerate time‑to‑demo and validate value** at the edge.

---

## 🧭 Positioning & Advantages (edge‑first)
- **Local‑first & offline‑tolerant**: on‑device inference, logs, KPIs (privacy‑preserving).
- **Open & modular**: Python + Streamlit with **plugin API**; no lock‑in.
- **Fast time‑to‑demo**: pre‑wired **17‑tab** dashboard (Traceability, Yield, Fleet, Benchmarks).
- **Lifecycle‑ready**: **Model Packs** (versioned) + **Fleet** (devices, deployments, events).
- **Best runtime per device**: **Benchmark Matrix** picks ONNX/OpenVINO/TensorRT by latency **and** accuracy.
- **From anomalies to rules**: **Triage** + **ROC/A‑B** to promote to deterministic pass/fail.

---

## 🚀 Core Features (merged)
- 🎥 **Multi‑modal inputs** — camera streams + industrial signals (USB/RTSP/GigE, GPIO/RS232)*
- 🔌 **Industrial protocols** — MQTT, Modbus/OPC‑UA placeholders, CANbus (where applicable)*
- 📊 **Dashboard** — Streamlit with **17 tabs** (three SQL‑backed analytics pages)
- 🔄 **Model lifecycle** — **Model Packs** + staged/shadow/rollback policies; deploy/rollback to devices
- 🧪 **Benchmarking** — record & select best runtime/shape per device
- 🧰 **Anomaly & Explainability** — saliency/XAI hooks; promote anomaly → rule
- 🧯 **Agents** — system recovery, adapter autogen, release notes (CLI)
- 📦 **Packaging** — Dockerfile + docker‑compose; GitHub Actions scaffold
- 📤 **Data export** — CSV/Parquet; MQTT sidecar stub for MES/Cloud

\* Some connectors and live pipelines are provided as **stubs** ready to wire.

---

## 🗺️ Dashboard Tabs (17)
1. 🏁 Quick Start
2. 📦 Model Packs
3. 🛰️ **Fleet (SQL)**
4. 📊 Benchmark Matrix
5. 🔍 Inference
6. 📷 Multi‑Cam Feeds
7. 📁 Log Viewer
8. 📇 **Data Traceability (SQL)**
9. 🧰 Triage Queue
10. ✅ Inspection Rules
11. 📈 **Yield & Quality (SQL)**
12. 🧱 Pipeline Builder
13. ⚙️ I/O Connectors
14. 🔐 Governance
15. 🛠️ Few‑Shot Fine‑Tuning
16. 🧪 Health Check
17. 📂 Examples

> The three **SQL‑backed** tabs read from `data/edge.db`. The Log Viewer is a simple stub; most analytics live in the SQL pages.

---

## 🎯 Edge AI Applications (Vision is one of them)
- **Vision Inspection (Factory QA)** — multi‑camera inference, anomaly triage, promote‑to‑rule, **unit‑level traceability**, **yield dashboards**.
- **Industrial IoT Sensor Gateway** — MQTT/OPC‑UA/Modbus ingestion, PASS/FAIL triggers, PLC handshake, trend KPIs, export to BI.
- **Vehicle AI (Fleet / Transit / Logistics)** — on‑device vision + CAN/GNSS, event publishing, OTA model updates.
- **Smart‑City Edge** — edge vision + environmental sensors, privacy‑preserving analytics, intermittent‑connectivity friendly.

---

## ⚙️ Install & Run (deterministic)
```bash
# Create a virtualenv and install deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Initialize SQLite (idempotent)
python scripts/init_sqlite.py

# Launch dashboard
streamlit run app.py
```
If activation is blocked (or on CI), use explicit interpreter:
```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip setuptools wheel
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python scripts/init_sqlite.py
./.venv/bin/python -m streamlit run app.py
```

---

## 📊 Vision Inspection Workflow
1. **🧱 Pipeline Builder** → `recipes/pipeline.yaml` (pre → model → post → rules → outputs)
2. **📦 Model Packs** → import/validate; attach pipeline & benchmarks
3. **📊 Benchmark Matrix** → persist best runtime/size into the pack
4. **🛰️ Fleet** → staged/shadow rollout (policy on deployments)
5. **🔍 Inference / 📷 Multi‑Cam** → capture; **📁 Log Viewer** to inspect
6. **📇 Data Traceability** → unit‑level records (serial, station, shift, vendor, model@ver, result)
7. **🧰 Triage Queue** → prioritize & label; **Promote → ✅ Rule**
8. **📈 Yield & Quality** → Yield%, DPPM, Pareto, trend; iterate.

---

## 🗄️ Data conventions
- **Events:** `logs/events.jsonl` (one JSON per line; includes `ts`, `unit_id`, `result`, `station_id`, …)
- **Images:** `logs/anomalies|pass|fail|samples/*.jpg(.json)` where sidecar JSON includes metadata (timestamp, unit_id, station_id, camera_id, model@ver, result, defect, score, label).

---

## 📦 Model Pack schema (minimum)
`model_packs/<name>/<version>/modelpack.yaml`
```yaml
model_id: defect-detector
version: 1.2.0
artifacts:
  onnx: artifacts/model.onnx
runtime:
  preferred: onnxruntime
benchmarks:
  "2025-09-12":
    onnxruntime: {fps: 30.0, latency_ms: 33.0, size: "640"}
pipeline: recipes/pipeline.yaml
metrics: {f1: 0.82}
train: {data_commit: 25c1f3...}  # if using DVC/Git-LFS
```

---

## 🛠️ Project Structure (consolidated)
```
core/                 # SQLite schema + db helper (WAL mode)
dashboard/tabs/       # SQL-backed pages: traceability, yield, fleet
bench/                # Benchmark Matrix helpers (record + best_engine)
rules/                # ROC assist & A/B helpers
quality/              # Triage queue helpers
gateway/              # MQTT sidecar (stub for MES/Cloud)
plugins/              # Minimal plugin registry for custom steps
packaging/            # Dockerfile + docker-compose
scripts/              # init_sqlite.py, doctor.py
app.py                # Streamlit app (17 tabs pre-wired)
docs/                 # Comparison / migration docs (if present)
```

---

## 🧪 Automated Testing & CI
```bash
pytest tests/
```
- Logger tests; OTA model switch; agents coverage.
- GitHub Actions (`.github/workflows/`) is scaffolded for releases/validation.

---

## 🔧 Troubleshooting
- **Missing `core` module** → run from repo root or use explicit interpreter (`./.venv/bin/python scripts/init_sqlite.py`).
- **No data in SQL tabs** → publish sample inspections or run your camera pipeline; views read `data/edge.db`.
- **Streamlit table width** → use `width='stretch'` (already applied in SQL tabs).

---

## 📚 Additional Resources
- docs/LEGACY_MIGRATION.md — old → new paths & commands (optional helper)

---

## 📢 Community & Contact
- [Website](https://www.sintrones.com)
- [LinkedIn](https://www.linkedin.com/company/sintrones-technology-corp/posts/?feedView=all)
📬 Want a hardware demo kit? [Contact Sintrones](https://www.sintrones.com/contact/)

---

## 📄 License
MIT — suitable for research, pilots, and production starters.
