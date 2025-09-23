# app.py — Streamlit UI with 19 tabs (fully wired)
import os
import streamlit as st

# ---------- Page config ----------
st.set_page_config(page_title="Edge AI Starter Kit", page_icon="🤖", layout="wide")

# ---------- Imports for all tab renderers ----------
# Stub/implemented tabs we shipped:
from dashboard.quick_start import render_quick_start
from dashboard.inference_page import render_inference
from dashboard.live_camera import render_live_camera
from dashboard.multi_cam import render_multi_cam
from dashboard.fewshot_finetune import render_fewshot
from dashboard.health_check import render_health_check
from dashboard.examples_page import render_examples
from dashboard.mes_export_page import render_mes_export

# Existing project tabs:
from dashboard.log_viewer import render_log_viewer
from dashboard.benchmark_matrix_page import render_benchmark_matrix
from dashboard.model_packs import render_model_packs_page
from dashboard.rules_page import render_rules_page
from dashboard.pipeline_builder_page import render_pipeline_builder
from dashboard.io_connectors_page import render_io_connectors
from dashboard.triage_queue import render_triage_queue
from dashboard.governance_page import render_governance

# SQLite-backed versions (preferred)
try:
    from dashboard.tabs.yield_quality_sqlite import render_yield_quality_sqlite
except Exception:
    # fallback name if your repo used a different path
    from dashboards.yield_dashboard import render_yield_dashboard as render_yield_quality_sqlite

try:
    from dashboard.tabs.traceability_sqlite import render_traceability_sqlite
except Exception:
    # fallback to older page module
    from dashboard.traceability_page import render_traceability_page as render_traceability_sqlite

# Fleet: prefer sqlite tab; fallback to page
try:
    from dashboard.tabs.fleet_sqlite import render_fleet_sqlite
except Exception:
    from dashboard.fleet_page import render_fleet_page as render_fleet_sqlite

# ---------- Titles & dispatch ----------
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
    "📤 MES Export",
]

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
    "📤 MES Export": render_mes_export,
}

# ---------- Render tabs ----------
tabs = st.tabs(TAB_TITLES)
for tab, title in zip(tabs, TAB_TITLES):
    with tab:
        fn = DISPATCH.get(title)
        if not fn:
            st.error(f"No renderer wired for: {title}")
            continue
        try:
            fn()
        except Exception as e:
            import traceback
            st.error(f"⚠️ Error rendering '{title}': {e}")
            st.code(traceback.format_exc())

# Optional sidebar environment panel

# Optional footer
with st.sidebar.expander("ℹ️ Environment"):
    st.write("EDGE_DB_PATH:", os.getenv("EDGE_DB_PATH", "(unset)"))
    st.write("CWD:", os.getcwd())
