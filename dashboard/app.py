
import streamlit as st
import os

# Dashboard modules
from dashboard.benchmark_viewer import show_benchmark_viewer
from dashboard.log_viewer import show_log_viewer
from dashboard.status_panel import show_status_panel

st.set_page_config(page_title="Sintrones Edge AI Dashboard", layout="wide")
st.sidebar.title("📊 Dashboard Navigation")

choice = st.sidebar.radio("Select Module", [
    "🏁 Quick Start",
    "🧠 Train Model",
    "🔍 Inference Engine",
    "🎥 Multi-Camera Stream",
    "🧩 Explainability / XAI",
    "📜 Anomaly Logs",
    "🛠️ Few-Shot Fine-Tuning",
    "📈 Model Benchmarking",
    "❤️ System Health Check",
    "📷 Live Camera Feed",
    "📦 Traceability Index"
])

st.title("🧠 Sintrones Edge AI Dashboard")

if choice == "🏁 Quick Start":
    st.write("Welcome to the Sintrones AI Vision Gateway Starter Kit.")
    st.markdown("Use the sidebar to navigate modules such as training, inference, XAI, benchmarking, and health checks.")

elif choice == "🧠 Train Model":
    st.info("Training pipeline will be integrated here.")
    st.markdown("Run `trainer.py` to train models from dataset.")

elif choice == "🔍 Inference Engine":
    st.info("Run ONNX model and collect results.")
    st.markdown("Use `inference_kit.py` to run real-time inference.")

elif choice == "🎥 Multi-Camera Stream":
    st.info("Multi-camera streaming simulation.")
    st.markdown("Launch `multi_cam_streamer.py` for multiple feeds.")

elif choice == "🧩 Explainability / XAI":
    st.info("Saliency/XAI tools to visualize model attention.")
    st.markdown("Module: `xai_tools/saliency_map.py`")

elif choice == "📜 Anomaly Logs":
    show_log_viewer()

elif choice == "🛠️ Few-Shot Fine-Tuning":
    st.subheader("🛠️ On-Device Few-Shot Fine-Tuning")
    uploaded = st.file_uploader("Upload anomaly image", type=["jpg", "png"])
    if uploaded:
        st.image(uploaded)
        label = st.selectbox("Label this image as:", ["OK", "NG-Defect1", "NG-Defect2"])
        st.success(f"Labeled as: {label} (save to template for ONNX)")

elif choice == "📈 Model Benchmarking":
    show_benchmark_viewer()
    st.markdown("Includes ONNX & PyTorch runtime comparison.")

elif choice == "❤️ System Health Check":
    st.info("Runs diagnostic checks and dependency validations.")
    st.markdown("See: `tools/healthcheck.py`, `system_recovery_agent.py`")

elif choice == "📷 Live Camera Feed":
    st.info("Live camera preview placeholder.")
    st.markdown("Camera simulation in `camera_infer.py`")

elif choice == "📦 Traceability Index":
    st.info("Data traceability and log indexing.")
    st.markdown("Module: `data_traceability/traceability_indexer.py`")
