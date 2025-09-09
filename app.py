
import os
import sys
import streamlit as st
import importlib.util

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# Imports with fallback
try:
    from examples.example_runner import run_example_scripts
    from ai_workflow.trainer import train_model
    from inference_engine.predictor import run_inference
    from multi_camera_support.multi_cam_streamer import get_mock_camera_feeds
    from xai_utils.saliency import save_saliency_map
    from data_traceability.log_store import store_log
    from fine_tune_ui.labeler import launch_finetune_interface
    from benchmarking.benchmark_panel import render_benchmark_panel
    from health_monitor.health_check import render_health_status
except ImportError:
    st.warning("Some modules failed to import. Please validate imports and folder names.")

st.set_page_config(page_title="Sintrones Edge AI Dashboard", layout="wide")
st.title("📡 Sintrones Edge AI Dashboard")

tabs = st.tabs(['🏁 Quick Start', '📂 Examples', '🧠 Train Model', '🔍 Inference', '🎥 Live Camera Feed', '🔥 Saliency / XAI', '📜 Data Traceability', '📁 Log Viewer', '🛠️ AI Fine-Tuning', '📊 Model Benchmarking', '🧪 Health Check'])

with tabs[0]:
    st.subheader("🏁 Quick Start Overview")
    st.markdown("This dashboard unifies edge AI workflows: training, inference, benchmarking, multi-cam feeds, explainability, and log traceability.")

with tabs[1]:
    st.subheader("📂 Run Sample Examples")
    try:
        run_example_scripts()
    except Exception as ex:
        st.error(f"Error in examples: {ex}")

with tabs[2]:
    st.subheader("🧠 Train a New Model")
    try:
        train_model()
    except Exception as ex:
        st.error(f"Training failed: {ex}")

with tabs[3]:
    st.subheader("🔍 Inference Engine")
    try:
        run_inference()
    except Exception as ex:
        st.error(f"Inference error: {ex}")

with tabs[4]:
    st.subheader("🎥 Live Camera Feed")
    try:
        feeds = get_mock_camera_feeds()
        for i, feed in enumerate(feeds):
            st.image(feed, caption=f"Camera {i+1}")
    except Exception as ex:
        st.error(f"Camera error: {ex}")

with tabs[5]:
    st.subheader("🔥 Saliency / XAI Visuals")
    try:
        import cv2
        img_path = os.path.join("logs", "assets", "cam1_feed.jpg")
        dummy = cv2.imread(img_path)
        if dummy is not None:
            sal = save_saliency_map(dummy, "logs/saliency_map.jpg")
            st.image(sal, caption="Saliency Map")
        else:
            st.warning("Missing: logs/assets/cam1_feed.jpg")
    except Exception as ex:
        st.error(f"XAI error: {ex}")

with tabs[6]:
    st.subheader("📜 Data Traceability")
    try:
        store_log("vision_pipeline", { "status": "demo log" })
        st.success("📦 Logs successfully simulated.")
    except Exception as ex:
        st.error(f"Traceability error: {ex}")

with tabs[7]:
    st.subheader("📁 Log File Viewer")
    try:
        log_files = os.listdir("logs")
        for lf in log_files:
            st.write(f"- {lf}")
    except Exception as ex:
        st.error(f"Log viewer error: {ex}")

with tabs[8]:
    st.subheader("🛠️ AI Fine-Tuning")
    try:
        launch_finetune_interface()
    except Exception as ex:
        st.error(f"Fine-tune error: {ex}")

with tabs[9]:
    st.subheader("📊 Model Benchmarking")
    try:
        render_benchmark_panel()
    except Exception as ex:
        st.error(f"Benchmark error: {ex}")

with tabs[10]:
    st.subheader("🧪 Health Check & Diagnostics")
    try:
        render_health_status()
    except Exception as ex:
        st.error(f"Health check error: {ex}")
