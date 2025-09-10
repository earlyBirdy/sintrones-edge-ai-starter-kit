
import os
import sys
import streamlit as st

# Setup path for local imports
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# Attempt imports with fallbacks
try:
    from examples.example_runner import run_example_scripts
except:
    run_example_scripts = lambda: st.warning("🚧 Example runner not available.")

try:
    from ai_workflow.trainer import train_model
except:
    train_model = lambda: st.warning("🚧 Training module not available.")

try:
    from inference_engine.predictor import run_inference
except:
    run_inference = lambda: st.warning("🚧 Inference module not available.")

try:
    from multi_camera_support.multi_cam_streamer import get_mock_camera_feeds
except:
    get_mock_camera_feeds = lambda: ["Camera1 Feed (mock)", "Camera2 Feed (mock)"]

try:
    from xai_tools.saliency_map import save_saliency_map
except:
    save_saliency_map = lambda: st.warning("🚧 Saliency module not available.")

try:
    from data_traceability.traceability_indexer import index_logs
except:
    index_logs = lambda: st.warning("🚧 Traceability module not available.")

try:
    from dashboard.log_viewer import show_log_viewer
except:
    show_log_viewer = lambda: st.warning("🚧 Log Viewer module not available.")

try:
    from dashboard.fine_tune_ui import render as show_finetune_ui
except:
    show_finetune_ui = lambda: st.warning("🚧 Fine-Tune UI not available.")

try:
    from dashboard.benchmark_viewer import show_benchmark_viewer
except:
    show_benchmark_viewer = lambda: st.warning("🚧 Benchmark Viewer not available.")

try:
    from dashboard.status_panel import show_status_panel
except:
    show_status_panel = lambda: st.warning("🚧 Status panel not available.")

try:
    from tools.healthcheck import run_healthcheck
except:
    run_healthcheck = lambda: st.warning("🚧 Health check tool not available.")

# Page Setup
st.set_page_config(page_title="Sintrones Edge AI Dashboard", layout="wide")
st.title("🧠 Sintrones Edge AI Dashboard")

# Navigation Tabs
tabs = st.tabs([
    '🏁 Quick Start', '📂 Examples', '🧠 Train Model', '🔍 Inference',
    '🎥 Live Camera Feed', '📷 Multi-Cam Feeds', '🔥 Saliency / XAI',
    '📜 Data Traceability', '📁 Log Viewer', '🛠️ AI Fine-Tuning',
    '📊 Benchmarking', '❤️ OTA/System Status', '🧪 Health Check'
])

with tabs[0]:
    st.subheader("🏁 Quick Start Overview")
    st.markdown("Welcome to the Sintrones AI Vision Gateway Starter Kit Dashboard.")

with tabs[1]:
    st.subheader("📂 Launch Example Scripts")
    run_example_scripts()

with tabs[2]:
    st.subheader("🧠 Train AI Model")
    train_model()

with tabs[3]:
    st.subheader("🔍 Inference Engine")
    run_inference()

with tabs[4]:
    st.subheader("🎥 Live Camera Feed")
    st.info("🚧 Live feed not connected. Use simulated camera or upload feed.")

with tabs[5]:
    st.subheader("📷 Multi-Camera Feeds")
    cams = get_mock_camera_feeds()
    for cam in cams:
        st.write(cam)

with tabs[6]:
    st.subheader("🔥 Saliency / Explainability")
    save_saliency_map()

with tabs[7]:
    st.subheader("📜 Data Traceability")
    index_logs()

with tabs[8]:
    st.subheader("📁 Anomaly Log Viewer")
    show_log_viewer()

with tabs[9]:
    st.subheader("🛠️ Few-Shot Fine-Tuning")
    show_finetune_ui()

with tabs[10]:
    st.subheader("📊 Model Benchmark Panel")
    show_benchmark_viewer()

with tabs[11]:
    st.subheader("❤️ OTA / System Status")
    show_status_panel()

with tabs[12]:
    st.subheader("🧪 System Health Check")
    run_healthcheck()
