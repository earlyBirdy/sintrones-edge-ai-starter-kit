import os, sys, subprocess
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# Optional imports (existing modules)
try:
    from dashboard.log_viewer import show_log_viewer
except Exception:
    show_log_viewer = None
try:
    from dashboard.status_panel import show_status_panel
except Exception:
    show_status_panel = None

# New pages
from dashboard.model_packs import render_model_packs_page
from dashboard.fleet_page import render_fleet_page
from dashboard.triage_queue import render_triage_queue
from dashboard.rules_page import render_rules_page
from dashboard.io_connectors_page import render_io_connectors
from dashboard.pipeline_builder_page import render_pipeline_builder
from dashboard.benchmark_matrix_page import render_benchmark_matrix
from dashboards.yield_dashboard import render_yield_dashboard
from dashboard.governance_page import render_governance

st.set_page_config(page_title="Sintrones Edge AI Dashboard", layout="wide")
st.title("🧠 Sintrones Edge AI Dashboard")

tabs = st.tabs([
    "🏁 Quick Start", "🔍 Inference", "🎥 Live Camera Feed", "📷 Multi-Cam Feeds",
    "📁 Log Viewer", "📊 Benchmark Matrix", "📈 Yield & Quality", "📦 Model Packs", "🛰️ Fleet",
    "✅ Inspection Rules", "🧱 Pipeline Builder", "⚙️ I/O Connectors",
    "🧰 Triage Queue", "🔐 Governance", "🛠️ Few-Shot Fine-Tuning", "🧪 Health Check", "📂 Examples"
])

with tabs[0]:
    st.subheader("🏁 Quick Start")
    st.write("AI-first layout with Model Packs, Fleet, Triage, Rules, and more.")

with tabs[1]:
    st.subheader("🔍 Inference")
    st.info("Hook your existing ai_workflow/inference_kit.py here.")

with tabs[2]:
    st.subheader("🎥 Live Camera Feed")
    st.info("Connect real camera stream or preview frames.")

with tabs[3]:
    st.subheader("📷 Multi-Cam Feeds")
    st.info("Configure RTSP/GigE/USB cameras and sync.")

with tabs[4]:
    st.subheader("📁 Anomaly Log Viewer")
    if show_log_viewer: show_log_viewer()
    else: st.warning("dashboard/log_viewer.py missing.")

with tabs[5]:
    render_benchmark_matrix()

with tabs[6]:
    render_yield_dashboard()

with tabs[7]:
    render_model_packs_page()

with tabs[8]:
    render_fleet_page()

with tabs[9]:
    render_rules_page()

with tabs[10]:
    render_pipeline_builder()

with tabs[11]:
    render_io_connectors()

with tabs[12]:
    render_triage_queue()

with tabs[13]:
    render_governance()

with tabs[14]:
    st.subheader("🛠️ Few-Shot Fine-Tuning")
    st.info("Upload a few images, label, and export a delta for ONNX update.")

with tabs[15]:
    st.subheader("🧪 System Health Check")
    if st.button("Run Healthcheck"):
        script = os.path.join(ROOT_DIR, "tools", "healthcheck.py")
        if os.path.exists(script):
            try:
                out = subprocess.check_output([sys.executable, script], cwd=ROOT_DIR, stderr=subprocess.STDOUT, text=True)
                st.code(out, language="json")
            except subprocess.CalledProcessError as e:
                st.error("Healthcheck failed:"); st.code(e.output)
        else:
            st.warning("tools/healthcheck.py not found.")

with tabs[16]:
    st.subheader("📂 Examples")
    examples = []
    for r, _, fs in os.walk(os.path.join(ROOT_DIR,"examples")):
        for f in fs:
            if f.endswith(".py"):
                examples.append(os.path.relpath(os.path.join(r,f), ROOT_DIR))
    if examples:
        for e in sorted(examples): st.code(f"python {e}")
    else:
        st.info("No examples found.")
