# 📦 Sintrones Edge AI Starter Kit
![Test Status](https://github.com/earlyBirdy/sintrones-edge-ai-starter-kit/actions/workflows/python-ci.yml/badge.svg)

**Edge AI Vision Inspection + Industrial IoT Sensor Gateway (Vehicle / Factory / City)**

A production‑minded, open framework to build **Edge AI** systems that combine **vision inspection**, **sensor telemetry**, and **industrial I/O** on rugged hardware. It ships a **Streamlit dashboard** (19+ tabs), a **SQLite backbone**, **Model Packs**, **Fleet**, and a **Benchmark Matrix** to accelerate PoCs → pilots → deployments.

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
- **Fast time‑to‑demo**: pre‑wired **19‑tab** dashboard (Traceability, Yield, Fleet, Benchmarks).
- **Lifecycle‑ready**: **Model Packs** (versioned) + **Fleet** (devices, deployments, events).
- **Best runtime per device**: **Benchmark Matrix** picks ONNX/OpenVINO/TensorRT by latency **and** accuracy.
- **From anomalies to rules**: **Triage** + **ROC/A‑B** to promote to deterministic pass/fail.

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
| **Standalone**   | Fully offline, single‑box; dashboard & sensor integration |
| **Edge-to-Cloud**| MQTT sync to MES/BI; CSV/Parquet export or other IoT platforms |
| **Vehicle AI**   | Add GPS/CANbus for on-road deployments       |
| **Containerized** | `docker compose -f packaging/docker-compose.yml up --build` |

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

## ✅ New Features
- **SQLite backbone** for on‑device metadata (devices, deployments, inspections, benchmarks, events, lineage) — default DB path **`data/edgekit.db`** (some builds use `data/edge.db`; both are supported).
- **SQL‑backed tabs**: **📇 Data Traceability**, **📈 Yield & Quality**, **🛰️ Fleet**.
- **Model Packs** with validate/smoke‑test hooks + policies for **staged/shadow/rollback**.
- **Benchmark Matrix** now schema‑agnostic (supports `engine` or `model`) and persists best runtime/size.
- **Triage Queue** wired to local anomalies with save/load state.
- New/verified modules per E2E probe: **Anomaly Log Viewer**, **Inference Balance**, **Benchmark Panel**, **Fine‑Tuning**, **Multi‑Camera**, **Saliency/XAI**, **Health Check**, **Inspection Rules**, **Pipeline Builder**, **I/O Connectors**, **Governance policy**, **Few‑Shot Fine‑Tuning**, **Examples**, **MES Export**.
- **ROC assist + A/B** helpers for setting inspection thresholds
- **Gateway sidecar (stub)** for MQTT→MES/Cloud and CDC table for safe sync
- **Plugin API** so integrators can add custom pre/post/rule steps
- **Dockerfile + docker‑compose** and a CI scaffold.
- **Probe summary:** 25 passed, 0 failed — see `probes/e2e_check.py`.

---

## 🗺️ Dashboard Tabs
1. 🏁 **Quick Start** — KPIs + latest inspections & events
2. 🔍 **Inference** — recent inference rows (schema‑adaptive)
3. 🎥 **Live Camera Feed** — lists endpoints from `config/cameras.yaml`
4. 📷 **Multi‑Cam Feeds** — 3‑column camera grid
5. 📁 **Log Viewer** — lookback filter; CSV/table; tail preview; download
6. 📊 **Benchmark Matrix** — best runtime/size persisted to DB
7. 📈 **Yield & Quality** — PASS/FAIL, Pareto, trend (SQL)
8. 📦 **Model Packs** — versioned packs, hooks, policies
9. 🛰️ **Fleet** — devices, deployments, events (SQL)
10. ✅ **Inspection Rules** — thresholds & rule sets
11. 🧱 **Pipeline Builder** — pre→model→post→rules→outputs
12. ⚙️ **I/O Connectors** — files, MQTT/MES stubs
13. 🧰 **Triage Queue** — anomalies → labeling → promote to rule
14. 🔐 **Governance** — policy, export guardrails
15. 🛠️ **Few‑Shot Fine‑Tuning** — list examples & spec
16. 🧪 **Health Check** — table existence/counts; filesystem checks
17. 📂 **Examples** — downloadable artifacts
18. 📇 **Data Traceability** — unit‑level lineage (SQL / compat view)
19. 📤 **MES Export** — `mes_latest.csv` export helper
## 🗺️ Dashboard Tabs (19)
> The three **SQL‑backed** tabs read from `data/edge.db`. The Log Viewer is a simple stub; most analytics live in the SQL pages.
---
Dashboard Tabs
**SQL‑backed analytics**
**Ops, lifecycle & dev**
**Capture & monitoring**
> Tabs render fully when their inputs/resources exist (DB rows, config files, folders). Placeholders are shown otherwise.
## 🧱 Project Structure (consolidated)
Project Structure (consolidated)
```
app.py                      # Streamlit app (tabs + dispatch)
core/                       # SQLite schema + db helper (WAL)
dashboard/                  # UI pages (incl. tabs/ for SQL)
bench/benchmark_matrix.py   # run_matrix(), record_benchmark(), best_engine()
quality/triage.py           # build_queue_from_anomalies(), save_queue(), add_triage_item()
rules/                      # ROC/A-B, rule helpers
gateway/                    # MQTT sidecar (stub)
pipelines/                  # pipeline configs
config/                     # cameras.yaml, inspection_rules.yaml, connectors/, policy.yaml
models/                     # finetune/, fewshot/, packs/
xai_results/                # saliency / XAI outputs
benchmarks/                 # benchmark artifacts
examples/                   # runnable examples
logs/                       # events.jsonl, anomalies/
data/edgekit.db             # primary SQLite (or data/edge.db in older builds)
---

Install & Run (deterministic)
```bash
# Create a virtualenv and install deps
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Initialize SQLite (idempotent)
python scripts/init_sqlite.py

# Launch dashboard
streamlit run app.py
```

---

End‑to‑End Dummy Data
Use the E2E seeder & probe to populate SQLite and validate tab queries quickly:
```bash
python tools/e2e/generate_dummy_data.py   # seeds devices, inspections, benchmarks, events
python tools/e2e/e2e_probe.py            # prints samples for the same queries the tabs use
```
After seeding, **Yield & Quality**, **Fleet**, **Data Traceability**, **Benchmark Matrix**, **Log Viewer** will show data.

---

## 🎯 Edge AI Applications
- **Vision Inspection (Factory QA)** — multi‑camera inference, anomaly triage, promote‑to‑rule, **unit‑level traceability**, **yield dashboards**.
- **Industrial IoT Sensor Gateway** — MQTT/OPC‑UA/Modbus ingestion, PASS/FAIL triggers, PLC handshake, trend KPIs, export to BI.
- **Vehicle AI (Fleet / Transit / Logistics)** — on‑device vision + CAN/GNSS, event publishing, OTA model updates.
- **Smart‑City Edge** — edge vision + environmental sensors, privacy‑preserving analytics, intermittent‑connectivity friendly.

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

## 🧰 Tooling & Utilities
- `e2e_bootstrap_pipeline_v31.py` — deterministic seeding for demos
- `tab_health_probe.py` — prints readiness of tables/folders for each tab
- `fix_streamlit_width_api.py` — repo‑wide Streamlit width migration
- `apply_ui_tweaks_env_footer.py` — remove/move the “Environment” panel
- `compat_views.sql` — safe views powering Inference & Traceability

---

## 🧪 Testing & CI
```bash
pytest tests/
```
- Agents, OTA model switch, loggers, schema adapters.
- GitHub Actions scaffolded in `.github/workflows/*`.

---

## 📚 Additional Resources
- docs/USE_CASES.md — real‑world factory/vehicle/city use cases
- docs/CONTRIBUTING.md — contribution workflow
- docs/LEGACY_MIGRATION.md — old → new paths & commands

---

📢 Community & Contact
- [Website](https://www.sintrones.com)
- [LinkedIn](https://www.linkedin.com/company/sintrones-technology-corp/posts/?feedView=all)
📬 Want a hardware demo kit? [Contact Sintrones](https://www.sintrones.com/contact/)

---

## 📄 License
MIT — suitable for research, pilots, and production starters.
