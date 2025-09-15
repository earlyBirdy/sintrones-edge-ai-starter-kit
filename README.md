# 📦 Sintrones Edge AI Starter Kit
**Edge AI Vision Inspection + Industrial IoT Sensor Gateway (Vehicle / Factory / City)**

A production‑minded, open framework to build **Edge AI** systems that combine **vision inspection**, **sensor telemetry**, and **industrial I/O** on rugged hardware. It ships a **Streamlit dashboard** (17 tabs), a **SQLite backbone**, **Model Packs**, **Fleet**, and a **Benchmark Matrix** to accelerate PoCs → pilots → deployments.

> **Vision Inspection is one of several Edge AI applications** supported by this kit.

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
- **Dockerfile + docker‑compose** and a CI scaffold

---

## 🎯 Edge AI Applications (Vision is one of them)
- **Vision Inspection (Factory QA)** — multi‑camera inference, anomaly triage, promote‑to‑rule, **unit‑level traceability**, **yield dashboards**.
- **Industrial IoT Sensor Gateway (Factory / Energy)** — MQTT/OPC‑UA/Modbus ingestion, PASS/FAIL triggers, PLC handshake, trend KPIs, export to BI.
- **Vehicle AI (Fleet / Transit / Logistics)** — on‑device vision + CAN/GNSS, event publishing, OTA model updates.
- **Smart‑City Edge** — edge vision + environmental sensors, privacy‑preserving analytics, intermittent‑connectivity friendly.

These use cases share the same modular core and dashboard.

---

## 🤝 Sales + Technical Collaboration
- 🛠️ Support System Integrators and SMEs with demo‑ready tools  
- 🤝 Collaborate on R&D and Proof‑of‑Concepts  
- 🌏 Promote industrial AI adoption across Thailand & SEA markets  

Use it as a base to build your own PoC, integrate with IIoT, or contribute modules — the repo helps you **accelerate time‑to‑demo and validate value** at the edge.

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

## 🧩 Key Modules & Layout (consolidated)
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
docs/                 # Comparison and usage docs (if present)
```
> Earlier paths like `dashboard/log_viewer.py`, `dashboards/`, or `ai_workflow/` may exist in older repos. In this consolidated layout use `app.py` + `dashboard/tabs/` + `core/`.

---

## 🧰 Vision Inspection Workflow
1. **🧱 Pipeline Builder** → `recipes/pipeline.yaml` (pre → model → post → rules → outputs)  
2. **📦 Model Packs** → import/validate; attach pipeline & benchmarks  
3. **📊 Benchmark Matrix** → persist best runtime/size into the pack  
4. **🛰️ Fleet** → staged/shadow rollout (policy on deployments)  
5. **🔍 Inference / 📷 Multi‑Cam** → capture; **📁 Log Viewer** to inspect  
6. **📇 Data Traceability** → unit‑level records (serial, station, shift, vendor, model@ver, result)  
7. **🧰 Triage Queue** → prioritize & label; **Promote → ✅ Rule**  
8. **📈 Yield & Quality** → Yield%, DPPM, Pareto, trend; iterate  

---

## 🗄️ Data Model (SQLite tables)
`devices`, `model_packs`, `deployments(policy)`, `sensor_readings`, `inspections`, `benchmarks`, `events`, `lineage`, and `changes` (CDC).  
Traceability joins `inspections` with pack/version to deliver lineage and KPIs.

---

## 📦 Model Pack (schema sketch)
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

## 🚢 Deployment Options
| Mode | Description |
|---|---|
| **Standalone** | Fully offline, single‑box |
| **Edge→Cloud** | MQTT sync to MES/BI; CSV/Parquet export |
| **Containerized** | `docker compose -f packaging/docker-compose.yml up --build` |

---

## 🧪 Automated Testing & CI
```bash
pytest tests/
```
GitHub Actions (`.github/workflows/`) is scaffolded for releases/validation.

---

## 🔧 Troubleshooting
- **Missing `core` module**: run from repo root or use explicit interpreter (`./.venv/bin/python scripts/init_sqlite.py`).
- **No data in SQL tabs**: publish sample inspections or run your camera pipeline; views read `data/edge.db`.
- **Streamlit table width**: use `width='stretch'` (already applied in SQL tabs).

---

## 📄 License
MIT — suitable for research, pilots, and production starters.
