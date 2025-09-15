
import streamlit as st

st.set_page_config(page_title="Sintrones Edge AI Starter Kit", layout="wide")

# ---- Imports for SQL‑backed tabs ----
from dashboard.tabs.traceability_sqlite import render_traceability_sqlite
from dashboard.tabs.yield_quality_sqlite import render_yield_quality_sqlite
from dashboard.tabs.fleet_sqlite import render_fleet_sqlite

# ---- Stubs for other tabs (safe fallbacks) ----
def render_quick_start():
    st.header("🏁 Quick Start", anchor=False)
    st.markdown("""
1. **Create venv & install**  
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Init SQLite**  
   ```bash
   python scripts/init_sqlite.py
   ```
3. **Run**  
   ```bash
   streamlit run app.py
   ```
    """)

def render_inference(): st.header("🔍 Inference", anchor=False); st.info("Hook your model runner here.")
def render_live_camera(): st.header("🎥 Live Camera Feed", anchor=False); st.info("Camera preview stub.")
def render_multicam(): st.header("📷 Multi-Cam Feeds", anchor=False); st.info("Multi-camera demo stub.")
def render_log_viewer(): st.header("📁 Log Viewer", anchor=False); st.info("Log viewer stub.")
def render_benchmark_matrix(): st.header("📊 Benchmark Matrix", anchor=False); st.info("Matrix view stub; see bench/benchmark_matrix.py")
def render_model_packs(): st.header("📦 Model Packs", anchor=False); st.info("Import/validate/deploy model packs UI stub.")
def render_inspection_rules(): st.header("✅ Inspection Rules", anchor=False); st.info("Rules UI stub (ROI + thresholds).")
def render_pipeline_builder(): st.header("🧱 Pipeline Builder", anchor=False); st.info("Low-code pipeline builder stub.")
def render_io_connectors(): st.header("⚙️ I/O Connectors", anchor=False); st.info("OPC-UA / Modbus / MQTT connectors stub.")
def render_triage_queue(): st.header("🧰 Triage Queue", anchor=False); st.info("Anomaly review queue stub.")
def render_governance(): st.header("🔐 Governance", anchor=False); st.info("Lineage & signing status stub.")
def render_few_shot(): st.header("🛠️ Few-Shot Fine-Tuning", anchor=False); st.info("Few-shot UI stub.")
def render_health_check(): st.header("🧪 Health Check", anchor=False); st.info("System & dependency checks stub.")
def render_examples(): st.header("📂 Examples", anchor=False); st.info("Example scripts and references.")

# ---- Tab order ----
tab_names = [
    "🏁 Quick Start","🔍 Inference","🎥 Live Camera Feed","📷 Multi-Cam Feeds","📁 Log Viewer",
    "📊 Benchmark Matrix","📈 Yield & Quality","📦 Model Packs","🛰️ Fleet","✅ Inspection Rules",
    "🧱 Pipeline Builder","⚙️ I/O Connectors","🧰 Triage Queue","🔐 Governance","🛠️ Few-Shot Fine-Tuning",
    "🧪 Health Check","📂 Examples","📇 Data Traceability"
]

tabs = st.tabs(tab_names)

# Map each tab to its renderer
renderers = [
    render_quick_start, render_inference, render_live_camera, render_multicam, render_log_viewer,
    render_benchmark_matrix, render_yield_quality_sqlite, render_model_packs, render_fleet_sqlite, render_inspection_rules,
    render_pipeline_builder, render_io_connectors, render_triage_queue, render_governance, render_few_shot,
    render_health_check, render_examples, render_traceability_sqlite
]

# Render with context managers so only the active tab draws
for t, render in zip(tabs, renderers):
    with t:
        render()
