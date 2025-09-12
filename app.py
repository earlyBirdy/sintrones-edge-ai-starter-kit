import os, sys, subprocess
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ---------- Safe imports with fallbacks ----------
try:
    from dashboard.log_viewer import show_log_viewer  # may accept show_title
except Exception:
    show_log_viewer = None

def _missing(msg: str):
    st.warning(msg)

def _stub(name):
    def _f():
        _missing(f"{name} page not available.")
    return _f

try:
    from dashboard.model_packs import render_model_packs_page
except Exception:
    render_model_packs_page = _stub("📦 Model Packs")

try:
    from dashboard.fleet_page import render_fleet_page
except Exception:
    render_fleet_page = _stub("🛰️ Fleet")

try:
    from dashboard.benchmark_matrix_page import render_benchmark_matrix
except Exception:
    render_benchmark_matrix = _stub("📊 Benchmark Matrix")

try:
    from dashboard.traceability_page import render_traceability_page
except Exception:
    def render_traceability_page():
        st.subheader("📜 Data Traceability")
        st.info("Traceability page missing. Ensure dashboard/traceability_page.py exists and is importable.")
        st.code("from dashboard.traceability_page import render_traceability_page", language="python")

try:
    from dashboard.triage_queue import render_triage_queue
except Exception:
    render_triage_queue = _stub("🧰 Triage Queue")

try:
    from dashboard.rules_page import render_rules_page
except Exception:
    render_rules_page = _stub("✅ Inspection Rules")

# Optional pages (best-effort)
try:
    from dashboards.yield_dashboard import render_yield_dashboard
except Exception:
    render_yield_dashboard = _stub("📈 Yield & Quality")

try:
    from dashboard.pipeline_builder_page import render_pipeline_builder
except Exception:
    render_pipeline_builder = _stub("🧱 Pipeline Builder")

try:
    from dashboard.io_connectors_page import render_io_connectors
except Exception:
    render_io_connectors = _stub("⚙️ I/O Connectors")

try:
    from dashboard.governance_page import render_governance
except Exception:
    render_governance = _stub("🔐 Governance")

# ---------- App layout ----------
st.set_page_config(page_title="Sintrones Edge AI Dashboard", layout="wide")
st.title("🧠 Sintrones Edge AI Dashboard")

tabs = st.tabs([
    "🏁 Quick Start", "📦 Model Packs", "🛰️ Fleet", "📊 Benchmark Matrix",
    "🔍 Inference", "📷 Multi-Cam Feeds", "📁 Log Viewer", "📜 Data Traceability",
    "🧰 Triage Queue", "✅ Inspection Rules", "📈 Yield & Quality", "🧱 Pipeline Builder",
    "⚙️ I/O Connectors", "🔐 Governance", "🛠️ Few-Shot Fine-Tuning", "🧪 Health Check", "📂 Examples"
])

with tabs[0]:
    st.subheader("🏁 Quick Start")
    st.write("AI-first layout: Model Packs → Fleet → Benchmark → Traceability → Triage → Rules → Yield.")

with tabs[1]:
    render_model_packs_page()

with tabs[2]:
    render_fleet_page()

with tabs[3]:
    render_benchmark_matrix()

with tabs[4]:
    st.subheader("🔍 Inference")
    st.info("Hook your existing ai_workflow/inference_kit.py here.")

with tabs[5]:
    st.subheader("📷 Multi-Cam Feeds")
    st.info("Configure RTSP/GigE/USB cameras and sync.")

with tabs[6]:
    # Log Viewer (render exactly one header)
    if show_log_viewer:
        try:
            show_log_viewer(show_title=True)
        except TypeError:
            st.subheader("📁 Anomaly Log Viewer")
            show_log_viewer()
    else:
        st.warning("dashboard/log_viewer.py missing.")

with tabs[7]:
    render_traceability_page()

with tabs[8]:
    render_triage_queue()

with tabs[9]:
    render_rules_page()

with tabs[10]:
    render_yield_dashboard()

with tabs[11]:
    render_pipeline_builder()

with tabs[12]:
    render_io_connectors()

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
                st.error("Healthcheck failed:")
                st.code(e.output)
        else:
            st.warning("tools/healthcheck.py not found.")

with tabs[16]:
    st.subheader("📂 Examples")
    examples = []
    for r, _, fs in os.walk(os.path.join(ROOT_DIR, "examples")):
        for f in fs:
            if f.endswith(".py"):
                examples.append(os.path.relpath(os.path.join(r, f), ROOT_DIR))
    if examples:
        for e in sorted(examples):
            st.code(f"python {e}")
    else:
        st.info("No examples found.")
