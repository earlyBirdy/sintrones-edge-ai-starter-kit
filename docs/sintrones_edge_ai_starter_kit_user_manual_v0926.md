# Sintrones Edge AI Starter Kit — User Manual (v2025-09-26)

A practical, step‑by‑step guide to get your 19‑tab Streamlit dashboard running end‑to‑end, understand what each tab does, and troubleshoot common issues.

---

## 0) System Requirements
- **Python** 3.10–3.12
- **OS**: macOS / Linux (Windows WSL is fine)
- **Streamlit** (installed via `requirements.txt`)
- **SQLite** CLI (optional, for manual checks)

---

## 1) Install & First Run

### 1.1 Create environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 1.2 Seed demo data (recommended)
The seeder populates the SQLite DB and creates folders/files that many tabs depend on.
```bash
python e2e_bootstrap_pipeline_v31.py
```
What it does:
- Populates `data/edgekit.db` (devices, inspections, events, benchmarks, anomalies)
- Creates folders: `logs/`, `logs/anomalies/`, `models/*`, `pipelines/`, `xai_results/`, `benchmarks/`, `examples/`
- Writes demo files (e.g., CSVs/logs) so filesystem‑based tabs have content

### 1.3 (Optional) Install compatibility views
These normalize columns expected by the UI when your DB is minimal or customized.
```bash
sqlite3 data/edgekit.db < sql/compat_views.sql
```
Creates:
- `inference_events_view(ts, device_id, engine, input_path, output_path, score)`
- `traceability_view(ts, unit_id, station, result, score, sensor_id)`

### 1.4 Launch the dashboard
```bash
streamlit run app.py
```
If a tab throws an error, it’s displayed inside that tab (traceback box). Use **Health Check** and **tab_health_probe.py** to verify prerequisites (see §4.3).

---

## 2) End‑to‑End Data Flow (high level)
1. **Devices & Sensors** produce readings / events
2. **Pipelines** run models → inference events, quality results
3. **Rules** & **Triage** convert anomalies into pass/fail rules
4. **Traceability** & **Yield** aggregate inspections
5. **Fleet** & **Log Viewer** provide operational visibility
6. **Benchmark Matrix** helps pick runtimes/models that fit latency/accuracy targets
7. **MES Export** hands results to downstream systems

**Primary DB:** `data/edgekit.db`  
**Environment variable:** `EDGE_DB_PATH` can override the DB location.

---

## 3) Tabs — How to Use (19)
Below: purpose → prerequisites → step‑by‑step → expected output → troubleshooting.

### 3.1 🏁 Quick Start
**Purpose:** Snapshot KPIs + latest activity.

**Prereq:** Seeded DB (`devices`, `inspections`, `events`, `benchmarks`, `anomalies`).

**Steps**
1) Open the tab.  
2) Review KPI tiles (Devices, Inspections, Events, Benchmarks, Anomalies).  
3) Scroll to **Recent Activity** (latest inspections, events).

**Expected:** Non‑zero counts and tables populated.

**Troubleshooting:** If empty, run `e2e_bootstrap_pipeline_v31.py` and check **🧪 Health Check**.

---

### 3.2 🔍 Inference
**Purpose:** Inspect recent inference records (schema‑adaptive).

**Prereq:** `inference_events_view` or `inference_events` (view recommended).

**Steps**
1) Use **Filters**: *Device contains*, *Engine contains* (if column exists), *Rows* limit.  
2) Scroll table; if `score` exists, review the line chart.

**Expected:** Table of inference rows; chart if numeric `score` exists.

**Troubleshooting:** If you see missing column errors, apply `sql/compat_views.sql` then reload.

---

### 3.3 🎥 Live Camera Feed
**Purpose:** List configured camera endpoints; hook up preview player later.

**Prereq:** `config/cameras.yaml`
```yaml
cameras:
  - id: cam0
    url: rtsp://...
```
**Steps**
1) Edit `config/cameras.yaml` with your sources.  
2) Reload the tab.

**Expected:** Card per camera with ID + URL.

**Troubleshooting:** If no file, the tab shows an example config and instructions.

---

### 3.4 📷 Multi‑Cam Feeds
**Purpose:** Grid view of multiple cameras.

**Prereq:** Same as §3.3.

**Steps**
1) Ensure `config/cameras.yaml` has 1+ cameras.  
2) Open the tab; feeds list in a 3‑column layout.

**Expected:** One tile per camera (placeholder description). Hook in your player as needed.

---

### 3.5 📁 Log Viewer
**Purpose:** Browse files in `./logs` with **Lookback hours** filter.

**Prereq:** `logs/` exists (the seeder creates it).

**Steps**
1) Set **Lookback hours** (default 24).  
2) Choose extensions, type a filename substring if needed.  
3) Toggle subdirectories & select a file.  
4) Preview: CSV renders as table; `.log/.jsonl/.txt` shows last N lines.  
5) Download the selected file.

**Expected:** A file table with size/modified time; a preview or note for header‑only CSVs.

**Troubleshooting:** If “No files match”, increase lookback, enable subdirs, or run the seeder.

---

### 3.6 📊 Benchmark Matrix
**Purpose:** Compare model/engine performance (fps, latency, accuracy).

**Prereq:** Rows in `benchmarks` (seeder adds sample rows).

**Steps**
1) Open tab; review the matrix/table and filters.  
2) Use it to pick best runtime by device/model.

**Expected:** Table or heat‑map style matrix of results.

**Troubleshooting:** If empty, insert rows into `benchmarks` or re‑run seeder.

---

### 3.7 📈 Yield & Quality (SQL)
**Purpose:** See pass/fail counts, yield trend, Pareto.

**Prereq:** Rows in `inspections`.

**Steps**
1) Select date range or limit; filter by result (PASS/FAIL).  
2) Explore trend/summary cards and the detail table.

**Expected:** Non‑zero pass/fail counts matching your seeded/demo data.

**Troubleshooting:** If empty, confirm `inspections` exists and has rows.

---

### 3.8 📦 Model Packs
**Purpose:** List versioned packs for deployment/testing.

**Prereq:** `models/packs/` with one or more pack folders.

**Steps**
1) Drop your pack(s) into `models/packs/<pack_name>/`.  
2) Refresh tab; click into a pack to review metadata.

**Expected:** List of pack names and basic info.

**Troubleshooting:** Ensure the folder exists and contains expected files.

---

### 3.9 🛰️ Fleet
**Purpose:** Device overview & heartbeat/events.

**Prereq:** `devices` + `events` rows.

**Steps**
1) Open tab; filter by device/time if available.  
2) Inspect event summaries for health/alerts.

**Expected:** List of devices and recent events.

**Troubleshooting:** Run the seeder; ensure your ingestion writes to `events`.

---

### 3.10 ✅ Inspection Rules
**Purpose:** Configure thresholds and rule sets.

**Prereq:** `config/inspection_rules.yaml`

**Steps**
1) Edit YAML to set limits/conditions (per station/model).  
2) Reload to apply; use **Triage** to promote findings into rules.

**Expected:** Rules list and effective thresholds.

**Troubleshooting:** Validate YAML syntax; keep a backup.

---

### 3.11 🧱 Pipeline Builder
**Purpose:** Compose capture → preproc → model → postproc → outputs.

**Prereq:** `pipelines/` contains one or more pipeline specs.

**Steps**
1) Place a pipeline YAML (e.g., `pipelines/demo.yaml`).  
2) Use the tab to inspect stages and IO bindings.

**Expected:** A stage list and connections. Adjust and re‑load as needed.

---

### 3.12 ⚙️ I/O Connectors
**Purpose:** Configure outbound/inbound connectors (Files, MQTT, MES).

**Prereq:** `config/connectors/` with connector configs.

**Steps**
1) Add connector definitions (e.g., file sinks, MQTT topics).  
2) Verify status in the tab.

**Expected:** Connector list with status/paths.

**Troubleshooting:** Check credentials/paths in YAML.

---

### 3.13 🧰 Triage Queue
**Purpose:** Review anomaly images and label/triage.

**Prereq:** Images in `logs/anomalies/*.jpg|*.png`.

**Steps**
1) Open queue; click an image.  
2) Mark as **Accept/Reject** (or tag defect) to guide future rules.

**Expected:** A list/grid of anomalies with actions.

**Troubleshooting:** Ensure the folder exists and contains images.

---

### 3.14 🔐 Governance
**Purpose:** View policy and export guardrails.

**Prereq:** `config/policy.yaml`.

**Steps**
1) Edit `policy.yaml` to set allowed exports/PII handling.  
2) Reload to enforce.

**Expected:** Policy fields displayed and used by export paths.

---

### 3.15 🛠️ Few‑Shot Fine‑Tuning
**Purpose:** Manage few‑shot examples/specs.

**Prereq:** `models/fewshot/` with images/labels/spec.

**Steps**
1) Drop small labeled sets into the folder.  
2) Review file list and example spec; kick off training externally.

**Expected:** File list and configuration snippet.

---

### 3.16 🧪 Health Check
**Purpose:** Sanity check DB tables and required folders/files.

**Prereq:** None (reads what exists).

**Steps**
1) Open tab; check table existence & row counts.  
2) Review filesystem checklist (logs, connectors, cameras, etc.).

**Expected:** Most items **OK** after seeding.

**Troubleshooting:** Missing items explain why other tabs are empty.

---

### 3.17 📂 Examples
**Purpose:** Download example assets quickly.

**Prereq:** `examples/` contains files.

**Steps**
1) Click the download button per item.

**Expected:** Browser downloads the file.

---

### 3.18 📇 Data Traceability (SQL)
**Purpose:** Unit‑level lineage and results over time.

**Prereq:** `traceability_view` or `inspections`.

**Steps**
1) Filter by **Unit ID contains**, **Only FAIL**, and row limit.  
2) Inspect the result table.

**Expected:** Recent units with result/score/station.

**Troubleshooting:** Apply `compat_views.sql` if columns are missing.

---

### 3.19 📤 MES Export
**Purpose:** Preview and download the latest MES CSV.

**Prereq:** `mes_latest.csv` in repo root.

**Steps**
1) Open tab; verify the CSV loads.  
2) Click **Download**.

**Expected:** A table preview and a working download button.

---

## 4) Troubleshooting & Maintenance

### 4.1 Common fixes
- **Tabs look identical** → Ensure `app.py` has a 1:1 `DISPATCH` (no `'lambda'` placeholders).
- **Only one tab works** → Seed the DB/folders (`e2e_bootstrap_pipeline_v31.py`).
- **DB errors** (`no such table/column`) → Apply `sql/compat_views.sql` for normalized views.
- **Two DB files** → Keep **one**: `data/edgekit.db` (optionally symlink `edge.db → edgekit.db`).
- **Log Viewer shows “ts,severity,type,message”** → That CSV has headers but no rows yet.

### 4.2 Useful commands
```bash
# Counts should be > 0 for most tabs
sqlite3 data/edgekit.db "SELECT COUNT(*) FROM inspections;"
sqlite3 data/edgekit.db "SELECT COUNT(*) FROM events;"
sqlite3 data/edgekit.db "SELECT COUNT(*) FROM benchmarks;"

# Table layouts
sqlite3 data/edgekit.db "PRAGMA table_info(inspections);"
sqlite3 data/edgekit.db "PRAGMA table_info(events);"
```

### 4.3 Health probe
Run the repo probe to check readiness for each feature:
```bash
python tab_health_probe.py
```

---

## 5) Project Structure (quick map)
```
app.py                      # 19 tabs + strict DISPATCH mapping
core/                       # schema & helpers
dashboard/                  # tab renderers
  tabs/                     # SQL‑backed pages (fleet/yield/traceability)
config/                     # cameras.yaml, inspection_rules.yaml, connectors/, policy.yaml
models/                     # finetune/, fewshot/, packs/
logs/                       # app.log, jsonl, anomaly_log.csv, anomalies/
benchmarks/                 # benchmark artifacts
xai_results/                # XAI results
pipelines/                  # pipeline YAMLs
examples/                   # sample assets
sql/                        # compat_views.sql
data/edgekit.db             # canonical SQLite DB
```

---

## 6) Supported Formats, Sensors/I/O, and Integrations

> This section clarifies **what works out‑of‑the‑box** vs **what’s scaffolded/stubbed** and **what’s easily pluggable** via adapters.

### 6.1 File Types (read / write)
| Category | Extensions / Types | Direction | Notes |
|---|---|---:|---|
| Images (vision) | `.jpg`, `.jpeg`, `.png`, `.bmp` | **Read** | Used by Triage Queue, Examples, Model Packs; typical 8‑bit RGB. |
| Video (optional) | RTSP/HTTP streams, local files `.mp4`, `.avi` | **Read** | Live/Multi‑Cam tabs list endpoints from `config/cameras.yaml`. Player hook is provided; decoding depends on your runtime. |
| Logs | `.log`, `.txt`, `.jsonl` | **Read** | Log Viewer tails/filters and previews last N lines. |
| Tables / CSV | `.csv` | **Read / Write** | Log Viewer previews CSV; MES Export writes `mes_latest.csv`. |
| SQLite DB | `edgekit.db` | **Read/Write** | Primary storage (devices, inspections, events, benchmarks, anomalies). |
| Config | `.yaml`, `.yml`, `.json` | **Read** | `config/` (cameras, rules, policy, connectors) and pipelines. |
| Models | `.onnx`, OpenVINO IR (`.xml/.bin`), TensorRT engine (`.engine`) | **Read** | Referenced by Model Packs / Pipelines. Inference runner is pluggable. |
| Artifacts | `xai_results/` (images, masks), `benchmarks/` | **Read** | Displayed by XAI/Benchmark tabs if present. |

> If you need **Parquet, Feather, or HDF5**: add a small loader in the relevant tab; Streamlit and pandas support them easily.

### 6.2 Sensors & I/O (Edge)
| Source / Sink | Status | How |
|---|---|---|
| **IP/USB/CSI Cameras** | ✅ Supported | Define in `config/cameras.yaml`. Live/Multi‑Cam tabs list them. Player hook included; you can swap in GStreamer/OpenCV/FFmpeg. |
| **Digital I/O / GPIO** | 🔷 Pluggable | Add a connector under `config/connectors/` and a small adapter (e.g., python‑periphery, RPi.GPIO). |
| **Serial (RS‑232/485)** | 🔷 Pluggable | Use `pyserial`; add an ingest script that writes into `events` or `sensor_readings`. |
| **CAN / J1939** | 🔷 Pluggable | Use `python‑can`/`cantools`; map frames to `sensor_readings(metric, value)` and/or `events`. |
| **GNSS / IMU** | 🔷 Pluggable | Ingest via serial/USB; persist to `sensor_readings` and visualize in custom tab. |
| **MQTT** | 🧩 Stub included | `gateway/` contains an MQTT sidecar stub; enable topics and map payloads → DB rows. |
| **Modbus‑TCP / RTU** | 🔷 Pluggable | Use `pymodbus`; read registers → `sensor_readings` / `events`. |
| **OPC‑UA** | 🔷 Pluggable | Use `opcua` python client; subscribe → DB. |

Legend: ✅ works now • 🧩 scaffold/stub provided • 🔷 easy to plug with a small adapter

**DB targets** for sensor ingests:
- Timeseries/metrics → `sensor_readings(ts, device_id, sensor_type, metric, value, unit)`
- Discrete events/alerts → `events(ts, device_id, severity, type, message, meta_json)`
- Quality results → `inspections(ts, device_id, unit_id, station, result, score, …)`

### 6.3 Back‑end / MES / IT Integrations
| Integration | Status | Direction | How |
|---|---|---:|---|
| **MES (CSV pickup)** | ✅ Supported | Out | Tab **📤 MES Export** writes `mes_latest.csv`. Point MES to poll this file or folder. |
| **HTTP/Webhook** | 🔷 Pluggable | Out | Add a tiny poster in the export step (e.g., `requests.post(...)`) and wire into Pipeline Builder or Rules. |
| **MQTT broker** | 🧩 Stub | In/Out | Use `gateway/` to publish/subscribe; map messages to DB or to rule outcomes. |
| **S3 / MinIO** | 🔷 Pluggable | Out | Use `boto3`/`minio` to push CSV, images, or JSON; call from MES Export or a pipeline sink. |
| **Database (Postgres/MySQL)** | 🔷 Pluggable | Out | Create a sync script to upsert from SQLite → RDBMS (e.g., `psycopg`, `mysqlclient`). |
| **OPC‑UA server** | 🔷 Pluggable | Out | Use `asyncua` to surface KPIs; feed from DB. |

> Start with the **CSV hand‑off** (most MES accept it), then evolve to webhook/MQTT if you need near‑real‑time.

### 6.4 Configuration Quick‑Refs
- **Cameras:** `config/cameras.yaml`  → used by Live/Multi‑Cam
- **Rules:** `config/inspection_rules.yaml` → used by Yield/Quality & Rules tab
- **Governance:** `config/policy.yaml` → used by Governance & Export paths
- **Connectors:** `config/connectors/` → stubs for MQTT/MES/files, extend as needed
- **Pipelines:** `pipelines/*.yaml` → end‑to‑end model flow; add sinks to DB/MQTT/HTTP

### 6.5 Input/Output Matrix per Tab
| Tab | Reads | Writes |
|---|---|---|
| Quick Start | `devices`, `inspections`, `events`, `benchmarks`, `anomalies` | — |
| Inference | `inference_events_view` or `inference_events` | — |
| Live/Multi‑Cam | `config/cameras.yaml` | — |
| Log Viewer | `logs/*` | — |
| Benchmark Matrix | `benchmarks` | — |
| Yield & Quality | `inspections` | — |
| Model Packs | `models/packs/*` | — |
| Fleet | `devices`, `events` | — |
| Inspection Rules | `config/inspection_rules.yaml` | — |
| Pipeline Builder | `pipelines/*` | — |
| I/O Connectors | `config/connectors/*` | — |
| Triage Queue | `logs/anomalies/*.{jpg,png}` | — |
| Governance | `config/policy.yaml` | — |
| Few‑Shot FT | `models/fewshot/*` | — |
| Health Check | DB tables + filesystem | — |
| Examples | `examples/*` | — |
| Data Traceability | `traceability_view` or `inspections` | — |
| MES Export | `mes_latest.csv` | `mes_latest.csv` |

---

## 7) FAQ
- **Where do I point the DB?** Set `EDGE_DB_PATH` or place DB at `data/edgekit.db`.
- **How do I add a new camera?** Edit `config/cameras.yaml`.
- **How do I export to MES?** Use **📤 MES Export**; it writes `mes_latest.csv`.
- **Why does a tab show nothing?** Check **🧪 Health Check** and run the seeder; ensure required tables/folders exist.

---
