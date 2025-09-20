# INSTALL — Sintrones Edge AI Starter Kit

**Last updated:** 2025-09-20

This guide merges and supersedes the two installation documents you shared, and adds the new E2E data-flow/testing steps and fixes. It keeps the concise flow while preserving optional Docker/MQTT notes. (Sources: internal INSTALL + extended Installation Guide.)

## 1) Prerequisites
- Python **3.10+** (tested on **3.11**)
- pip 21+
- macOS / Ubuntu / WSL2
- Optional: GPU runtimes (OpenVINO / TensorRT)
- Optional: MQTT broker (Mosquitto) for sidecar tests
- Optional: `sqlite3` CLI for quick checks

## 2) Create a virtual environment
```bash
python3 -m venv .venv && source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

## 3) Install dependencies
```bash
python -m pip install -r requirements.txt
```

## 4) Initialize / seed SQLite (choose one)
**A. Minimal init (idempotent)**
```bash
python scripts/init_sqlite.py
```
> The script adds the repo root to `sys.path` so it works regardless of the shell you use.

**B. E2E seed (recommended for demos)**
```bash
# Create DB with realistic rows used by the Streamlit tabs
python tools/e2e/generate_dummy_data.py

# Sanity probe: runs the same style of queries the tabs use
python tools/e2e/e2e_probe.py
```

(Alternatively, you can use the downloadable E2E bundle and run the same two scripts from that folder.)

## 5) Run the dashboard
```bash
streamlit run app.py
```
Open the printed **Local URL** in your browser. Always run from the **repo root** (same folder as `app.py`).

## 6) Optional: Docker (dashboard + MQTT broker)
```bash
docker compose -f packaging/docker-compose.yml up --build
```

## 7) Optional: Mosquitto locally
**macOS (Homebrew)**
```bash
brew install mosquitto && brew services start mosquitto
```
**Ubuntu**
```bash
sudo apt install -y mosquitto mosquitto-clients
```

---

## Feature inputs (so tabs aren’t empty)
- **Yield & Quality / Data Traceability** → rows in `inspections`
- **Fleet / Log Viewer** → rows in `events`
- **Benchmark Matrix** → rows in `benchmarks`
- **Triage Queue** → place a few `.jpg`/`.png` under `logs/anomalies/**`
- **Model Packs / Governance** → add directories/files under `model_packs/**`

> Tip: The E2E seeder populates all DB-backed tables so the data tabs render immediately.

## Troubleshooting
- **Activation issues** — use explicit interpreter:
  ```bash
  python3 -m venv .venv
  ./.venv/bin/python -m pip install --upgrade pip setuptools wheel
  ./.venv/bin/python -m pip install -r requirements.txt
  ./.venv/bin/python scripts/init_sqlite.py
  ./.venv/bin/python -m streamlit run app.py
  ```
- **ImportError on `from dashboard.*`** — start Streamlit from repo root.
- **Empty pages** — seed the DB or add the local files listed in *Feature inputs*.
- **Streamlit deprecations** —
  - Replace `st.experimental_rerun()` with `st.rerun()`
  - Replace `use_container_width` with `width='stretch'|'content'`

### Quick DB sanity checks
```bash
sqlite3 data/edge.db "SELECT COUNT(*) FROM inspections;"
sqlite3 data/edge.db "SELECT COUNT(*) FROM events;"
sqlite3 data/edge.db "SELECT COUNT(*) FROM benchmarks;"
```

## What’s new in this release
- Unified tab dispatch in `app.py` and a generic tab renderer loop
- `bench/benchmark_matrix.py::run_matrix()` with schema-agnostic helpers
- Triage helpers in `quality/triage.py` and updated `dashboard/triage_queue.py`
- Fixed `dashboard/governance_page.py` code-block syntax; added helpful placeholders
- E2E dummy-data seeder + probe for quick end-to-end testing
