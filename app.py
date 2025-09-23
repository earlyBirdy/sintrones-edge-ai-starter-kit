#!/usr/bin/env python3
# app.py — Streamlit UI with always-on tabs wired to e2e checks
# Adds: sidebar lookback selector + TEMP view `v_trace_window` (per-run)
#       + 📤 MES Export tab with button and preview
#       + Streamlit API updates: st.rerun(), width='stretch'

import os
import importlib
import sqlite3
from contextlib import contextmanager
from pathlib import Path
import csv

import streamlit as st

# ------------------------------------------------------------
# Sidebar: pick the lookback window (hours)
# ------------------------------------------------------------
DEFAULT_LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "24"))

choice = st.sidebar.selectbox(
    "Lookback window",
    ["24 hours", "7 days", "30 days", "Custom…"],
    index=2 if DEFAULT_LOOKBACK_HOURS >= 720 else (1 if DEFAULT_LOOKBACK_HOURS >= 168 else 0),
)

if choice == "24 hours":
    LOOKBACK_HOURS_UI = 24
elif choice == "7 days":
    LOOKBACK_HOURS_UI = 7 * 24
elif choice == "30 days":
    LOOKBACK_HOURS_UI = 30 * 24
else:
    LOOKBACK_HOURS_UI = st.sidebar.number_input(
        "Custom hours", min_value=1, value=DEFAULT_LOOKBACK_HOURS, step=1
    )

st.sidebar.caption(f"Using lookback: **{LOOKBACK_HOURS_UI} hours**")

# Make the chosen window available to probe checks (they read from env)
os.environ["LOOKBACK_HOURS"] = str(LOOKBACK_HOURS_UI)

# ------------------------------------------------------------
# DB utilities + per-run TEMP view creation
# ------------------------------------------------------------
DB_PATH = os.getenv("EDGEKIT_DB_PATH", "data/edgekit.db")

@contextmanager
def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()

def create_trace_view(hours: int):
    """Create a per-run TEMP view that all tabs can use for consistent time filtering."""
    with db() as c:
        c.execute("DROP VIEW IF EXISTS v_trace_window;")
        c.execute(f"""
            CREATE TEMP VIEW v_trace_window AS
            SELECT
              sr.id            AS reading_id,
              sr.device_id,
              sr.ts            AS sr_ts,        -- UTC
              ie.ts            AS inf_ts,
              ie.pred_label,
              ie.score,
              qr.ts            AS qual_ts,
              qr.passed        AS qual_passed,
              a.ts             AS anom_ts,
              a.severity
            FROM sensor_readings sr
            LEFT JOIN inference_events ie ON ie.reading_id = sr.id
            LEFT JOIN quality_results  qr ON qr.reading_id = sr.id
            LEFT JOIN anomalies        a  ON a.reading_id  = sr.id
            WHERE sr.ts >= datetime('now','-{hours} hours');
        """)
create_trace_view(LOOKBACK_HOURS_UI)

# ------------------------------------------------------------
# Import/reload probe checks AFTER setting LOOKBACK_HOURS
# ------------------------------------------------------------
import probes.e2e_check as e2e_check
e2e_check = importlib.reload(e2e_check)   # ensure it picks up the updated LOOKBACK_HOURS
from probes.e2e_check import CHECKS, _conn  # reuse check registry and DB connector

# MES exporter (schema-aware)
from probes.mes_exporter import run_export


# === Injected by ChatGPT: dashboard dispatch wiring ===
from dashboard.log_viewer import render_log_viewer
from dashboard.benchmark_matrix_page import render_benchmark_matrix
from dashboard.tabs.yield_quality_sqlite import render_yield_quality_sqlite
from dashboard.model_packs import render_model_packs_page
from dashboard.tabs.fleet_sqlite import render_fleet_sqlite
from dashboard.rules_page import render_rules_page
from dashboard.pipeline_builder_page import render_pipeline_builder
from dashboard.io_connectors_page import render_io_connectors
from dashboard.triage_queue import render_triage_queue
from dashboard.governance_page import render_governance
from dashboard.status_panel import show_status_panel
from dashboard.tabs.traceability_sqlite import render_traceability_sqlite
from dashboard.quick_start import render_quick_start
from dashboard.inference_page import render_inference
from dashboard.live_camera import render_live_camera
from dashboard.multi_cam import render_multi_cam
from dashboard.fewshot_finetune import render_fewshot
from dashboard.health_check import render_health_check
from dashboard.examples_page import render_examples
from dashboard.mes_export_page import render_mes_export


def _placeholder(msg: str):
    import streamlit as st
    st.info(msg)

DISPATCH = {
    "🏁 Quick Start": render_quick_start,
    "🔍 Inference": render_inference,
    "🎥 Live Camera Feed": render_live_camera,
    "📷 Multi-Cam Feeds": render_multi_cam,
    "📁 Log Viewer": render_log_viewer,
    "📊 Benchmark Matrix": render_benchmark_matrix,
    "📈 Yield & Quality": render_yield_quality_sqlite,
    "📦 Model Packs": render_model_packs_page,
    "🛰️ Fleet": render_fleet_sqlite,
    "✅ Inspection Rules": render_rules_page,
    "🧱 Pipeline Builder": render_pipeline_builder,
    "⚙️ I/O Connectors": render_io_connectors,
    "🧰 Triage Queue": render_triage_queue,
    "🔐 Governance": render_governance,
    "🛠️ Few-Shot Fine-Tuning": render_fewshot,
    "🧪 Health Check": render_health_check,
    "📂 Examples": render_examples,
    "📇 Data Traceability": render_traceability_sqlite,
    "📤 MES Export": render_mes_export
}
# === end injection ===

# === Injected by ChatGPT: helper to render a tab by title ===
def _render_tab_by_title(title: str):
    import streamlit as st
    if title == "📤 MES Export":
        try:
            render_mes_export_ui_here()
        except Exception:
            st.info("MES Export UI not found in this build.")
        return
    fn = DISPATCH.get(title)
    if fn:
        fn()
    else:
        st.info("No renderer registered for this tab yet.")
# === end injection ===



# ------------------------------------------------------------
# App config
# ------------------------------------------------------------
st.set_page_config(page_title="Edge AI Starter Kit", page_icon="🏁", layout="wide")

# Single source of truth: ALL tabs you want visible now (add more anytime)
TAB_TITLES = [
    "🏁 Quick Start",
    "🔍 Inference",
    "🎥 Live Camera Feed",
    "📷 Multi-Cam Feeds",
    "📁 Log Viewer",
    "📊 Benchmark Matrix",
    "📈 Yield & Quality",
    "📦 Model Packs",
    "🛰️ Fleet",
    "✅ Inspection Rules",
    "🧱 Pipeline Builder",
    "⚙️ I/O Connectors",
    "🧰 Triage Queue",
    "🔐 Governance",
    "🛠️ Few-Shot Fine-Tuning",
    "🧪 Health Check",
    "📂 Examples",
    "📇 Data Traceability",
    "📤 MES Export",          # NEW
]

# Map UI titles → check names in CHECKS (so every tab is “active”)
UI_TO_CHECK = {
    "🏁 Quick Start": "Quick Start",
    "🔍 Inference": "Inference Balance",
    "🎥 Live Camera Feed": "Multi-Camera",          # reuses camera config presence
    "📷 Multi-Cam Feeds": "Multi-Camera",
    "📁 Log Viewer": "Logs",
    "📊 Benchmark Matrix": "Benchmark Panel",
    "📈 Yield & Quality": "Yield & Quality",
    "📦 Model Packs": "📦 Model Packs",
    "🛰️ Fleet": "Fleet",
    "✅ Inspection Rules": "✅ Inspection Rules",
    "🧱 Pipeline Builder": "🧱 Pipeline Builder",
    "⚙️ I/O Connectors": "⚙️ I/O Connectors",
    "🧰 Triage Queue": "🧰 Triage Queue",
    "🔐 Governance": "🔐 Governance",
    "🛠️ Few-Shot Fine-Tuning": "🛠️ Few-Shot Fine-Tuning",
    "🧪 Health Check": "Health Check",
    "📂 Examples": "📂 Examples",
    "📇 Data Traceability": "Data Traceability",
    "📤 MES Export": "MES Export",
}

MES_DIR = Path(os.getenv("MES_EXPORT_DIR", "exports/mes"))

# ------------------------------------------------------------
# Render helpers
# ------------------------------------------------------------
def status_badge(ok: bool) -> str:
    color = "green" if ok else "red"
    text = "PASS" if ok else "FAIL"
    return f"<span style='background:{color};color:white;padding:2px 8px;border-radius:999px;font-weight:600'>{text}</span>"

def _preview_mes_latest(max_rows: int = 50):
    latest = MES_DIR / "mes_latest.csv"
    if not latest.exists():
        st.warning("No `mes_latest.csv` found in exports/mes. Click export to generate.")
        return
    rows = []
    with latest.open() as f:
        rdr = csv.DictReader(f)
        for i, r in enumerate(rdr):
            if i >= max_rows: break
            rows.append(r)
    st.caption(f"Previewing `{latest.name}` (first {len(rows)} rows)")
    # UPDATED: use width='stretch' instead of use_container_width
    st.dataframe(rows, width='stretch')

def render_module(title: str):
    # Special handling for the MES Export tab
    if title == "📤 MES Export":
        st.subheader(title)
        st.caption(f"Export window is controlled by the sidebar: **{LOOKBACK_HOURS_UI} hours**")
        cols = st.columns([1,1,2])
        with cols[0]:
            # UPDATED: width='stretch' for buttons
            if st.button("Export to MES (CSV + JSON)", width='stretch'):
                info = run_export(LOOKBACK_HOURS_UI)
                st.success(f"Exported {info['rows']} rows")
                st.code(info, language="json")
        with cols[1]:
            if st.button("Refresh Preview", width='stretch'):
                # UPDATED: st.rerun replaces experimental_rerun
                st.rerun()
        st.divider()
        _preview_mes_latest()
        return

    # Normal path: use probe checks
    check_name = UI_TO_CHECK.get(title)
    fn = CHECKS.get(check_name) if check_name else None

    st.subheader(title)
    st.caption(f"Check: {check_name or '— (placeholder)'} • Window: {LOOKBACK_HOURS_UI}h")

    if fn is None:
        st.info("Feature is enabled. No formal health check wired yet; configure via config/ or models/ as needed.")
        return

    # Run the module check (DB/file-driven) and display a simple health card
    try:
        with _conn() as conn:
            ok, msg = fn(conn)
    except Exception as e:
        ok, msg = False, f"Check error: {e}"

    st.markdown(status_badge(ok), unsafe_allow_html=True)
    st.write(msg)

    # Optional: convenience query preview from the TEMP view (for data tabs)
# [peek_cleanup]     with st.expander("Peek v_trace_window (first 20 rows)"):
# [peek_cleanup]         try:
# [peek_cleanup]             with db() as con:
# [peek_cleanup]                 rows = con.execute("SELECT * FROM v_trace_window ORDER BY sr_ts DESC LIMIT 20").fetchall()
                # UPDATED: width='stretch' instead of use_container_width
# [peek_cleanup]                 st.dataframe([dict(r) for r in rows], width='stretch')
# [peek_cleanup]         except Exception as e:
# [peek_cleanup]             st.warning(f"Preview unavailable: {e}")
# [peek_cleanup]
    # Convenience: self-heal button for file-driven checks (creates placeholders)
    if not ok and st.button("Attempt auto-fix (create placeholders)", key=f"fix_{title}"):
        try:
            with _conn() as conn:
                ok2, msg2 = fn(conn)  # many file-driven checks create placeholders on first run
            # UPDATED: st.rerun replaces experimental_rerun
            st.rerun()
        except Exception as e:
            st.error(f"Auto-fix failed: {e}")

# ------------------------------------------------------------
# Build the tabs (always show ALL)
# ------------------------------------------------------------
tabs = st.tabs(TAB_TITLES)
for t, title in zip(tabs, TAB_TITLES):
    with t:
        render_module(title)