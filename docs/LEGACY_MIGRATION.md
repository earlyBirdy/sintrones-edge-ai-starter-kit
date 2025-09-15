# 📚 Legacy Migration Guide — Sintrones Edge AI Starter Kit

This guide helps you move from **older repo layouts** to the **current consolidated structure** delivered with the Sept 2025 update.

## TL;DR
- Single entrypoint: **`app.py`**
- SQL-backed tabs live in **`dashboard/tabs/`**
- On‑device metadata stored in **SQLite** at `data/edge.db` via **`core/`**
- Use **`scripts/init_sqlite.py`** to (re)create schema
- Prefer **venv + explicit interpreter** for reliability

---

## 1) Paths — *Old → New*

| Area | Old Path / Concept | New Path / Concept |
|---|---|---|
| App entrypoint | `dashboard/app.py` / `dashboard/dashboard.py` | **`app.py`** (root) with 17 tabs pre‑wired |
| Log viewer code | `dashboard/log_viewer.py` | **Stub in `app.py`** (analytics now in SQL tabs) |
| Traceability | `traceability_indexer.py` / ad‑hoc CSVs | **`dashboard/tabs/traceability_sqlite.py`** + **SQLite `inspections`** |
| Yield & Quality | bespoke notebooks / CSV exports | **`dashboard/tabs/yield_quality_sqlite.py`** (SQL) |
| Fleet/device lists | scripts under `orchestration/` | **`dashboard/tabs/fleet_sqlite.py`** + **SQLite `devices`,`deployments`,`events`** |
| Benchmark viewer | `dashboard/benchmark_viewer.py` | **`bench/benchmark_matrix.py`** + **tab in `app.py`** |
| Model packs | `orchestration/model_pack.py` | **DB tables `model_packs` & `deployments`** + **Model Packs tab (stub)** |
| Pipelines | `ai_workflow/` / scattered steps | **`plugins/api.py`** (extensibility) + **`recipes/pipeline.yaml`** (concept) |
| Governance/XAI bits | scattered utils | **`rules/roc_assist.py`** (thresholds, A/B) |
| MQTT / Cloud bridge | `cloud_bridge.py` / misc | **`gateway/bridge.py`** (MQTT→MES/Cloud stub) |
| Packaging | `docker/Dockerfile` | **`packaging/Dockerfile`** + **`packaging/docker-compose.yml`** |
| DB init | `init_db.py` or hand-written SQL | **`scripts/init_sqlite.py`** (path‑robust) |
| Project docs | README notes / wiki | **`docs/Comparison_Edge_AI_Inspection.md`** (consolidated) |

> If your older repo contains `dashboards/`, `ai_workflow/`, or `dashboard/log_viewer.py`, keep them only if you still depend on them. The new layout routes everything through **`app.py`** and SQL tabs.

---

## 2) Commands — *Old → New*

### Run the dashboard
- **Old**: `streamlit run dashboard/app.py` or `python -m streamlit run dashboard/app.py`  
- **New**:  
  ```bash
  streamlit run app.py
  ```

### Initialize storage
- **Old**: `python init_db.py` or manual SQL files  
- **New**:  
  ```bash
  python scripts/init_sqlite.py
  ```

### Create environment
- **Old**: `pip install -r requirements.txt` on system Python  
- **New (recommended)**:
  ```bash
  python3 -m venv .venv && source .venv/bin/activate
  pip install -r requirements.txt
  # or explicit interpreter:
  ./.venv/bin/python -m pip install -r requirements.txt
  ```

### Docker / Compose
- **Old**: `docker build -f docker/Dockerfile .`  
- **New**:
  ```bash
  docker compose -f packaging/docker-compose.yml up --build
  ```

---

## 3) Feature Equivalence

| Capability | Previous Approach | Current Approach |
|---|---|---|
| Per‑unit traceability | CSV/JSON logs / scripts | **SQLite `inspections`** + **Traceability tab** |
| Yield dashboards | Notebook/CSV | **Yield & Quality (SQL) tab** |
| Device/fleet view | Custom scripts | **Fleet (SQL) tab** |
| Benchmark selection | Manual | **Benchmark Matrix gating** (`bench/benchmark_matrix.py`) |
| Rules thresholds | Manual tuning | **ROC assist + A/B** (`rules/roc_assist.py`) |
| Few‑shot & triage | Ad‑hoc | **Triage events** (`quality/triage.py`) + UI stub |
| OTA & packs | JSON scripts | **DB‑tracked `model_packs`/`deployments`** + tab stub |
| Cloud/MES bridge | Custom code | **MQTT sidecar** (`gateway/bridge.py`) |

---

## 4) Streamlit UI Notes
- Use `width='stretch'` for tables (replaces deprecated `use_container_width=True`).
- Avoid duplicate tab headers (older builds sometimes showed *Anomaly Log Viewer* twice). Consolidated **`app.py`** fixes this.

---

## 5) Minimal Migration Checklist
1. Move your custom pages under **`dashboard/tabs/`** and expose a `render_*()` function.  
2. Store inspection results to **SQLite** (`core/db.py` → table `inspections`).  
3. Replace bespoke CSVs with queries in tabs; keep CSV export for BI if needed.  
4. Package your models as **Model Packs** (DB entries + artifacts on disk).  
5. Use **`bench/benchmark_matrix.py`** to record results and select the engine at deploy time.  
6. For cloud/MES, adapt **`gateway/bridge.py`** to your topic schema and auth.  
7. Pin installs to a **venv** or container for reproducibility.

---

## 6) FAQ
- **Can I still run old scripts?** Yes, but prefer routing through **`app.py`** and the SQL tabs for consistency.  
- **Where is the DB file?** `data/edge.db` (created by `scripts/init_sqlite.py`).  
- **Do I need Docker?** No; Docker/Compose is optional but handy for demos and sidecar services (MQTT).

---

If you hit a specific path that’s not covered here, share it and we’ll add it to the table.
