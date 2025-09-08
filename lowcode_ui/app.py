import streamlit as st
import subprocess
import time
import sys
import os

# Ensure parent directory is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai_workflow.trainer import train_model
from ai_workflow.inference_kit import run_inference
from data_traceability.log_store import store_log
from multi_camera_support.multi_cam_streamer import get_mock_camera_feeds
from xai_tools.saliency_map import generate_saliency

st.set_page_config(page_title="Sintrones Edge AI All-in-One Dashboard", layout="wide")
st.title("📊 Sintrones Edge AI Starter Kit — Unified Dashboard")

tabs = st.tabs([
    "🏁 Quick Start",
    "📂 Examples",
    "🧠 Train Model",
    "🔍 Inference",
    "🎥 Multi-Camera",
    "🧩 Explainability",
    "📜 Logs",
    "🛠️ Fine-Tune UI",
    "📈 Benchmark Panel",
    "❤️ Health Check"
])

with tabs[0]:
    st.header("Quick Start")
    st.markdown("""
- Run vision inspection apps with zero config  
- Test pretrained models  
- Access all modules from one place  
""")

with tabs[1]:
    st.header("Examples")
    st.code("python examples/factory_automation/factory_monitor.py", language='bash')
    st.code("python examples/vision_inspection/camera_infer.py", language='bash')

with tabs[2]:
    st.header("Train Model")
    data_path = st.text_input("Training Data Path", "data/train/")
    model_output = st.text_input("Model Output Path", "models/model.pth")
    if st.button("Train"):
        result = train_model(data_path, model_output)
        st.success(f"✅ Model trained and saved: {result}")

with tabs[3]:
    st.header("Run Inference")
    model_path = st.text_input("Model File", "models/model.pth")
    image_path = st.text_input("Image File", "samples/image1.jpg")
    if st.button("Infer"):
        result = run_inference(model_path, image_path)
        st.json(result)
        store_log(result)

with tabs[4]:
    st.header("Multi-Camera Feed")
    feeds = get_mock_camera_feeds()
    for idx, feed in enumerate(feeds):
        st.image(feed, caption=f"Camera {idx+1}")

with tabs[5]:
    st.header("Explainability Overlay")
    image_path_exp = st.text_input("Image for Saliency Map", "samples/image1.jpg")
    if st.button("Generate"):
        saliency = generate_saliency(image_path_exp)
        st.image(saliency, caption="Saliency Map")

with tabs[6]:
    st.header("Log & Traceability")
    st.info("🔍 Trace logs (placeholder): backend not connected to actual DB.")

with tabs[7]:
    st.header("🛠️ Fine-Tune UI")
    st.markdown("Upload a JSON/YAML template to simulate fine-tuning.")
    uploaded = st.file_uploader("Upload Few-Shot Template", type=["json", "yaml"])
    if uploaded:
        st.success("Uploaded successfully. Fine-tuning would start...")
        with st.spinner("Fine-tuning model..."):
            time.sleep(2)
        st.success("Fine-tune complete. New ONNX exported.")

with tabs[8]:
    st.header("📈 Benchmark Panel")
    st.markdown("Run ONNX vs PyTorch speed comparison (simulated).")
    runtimes = ["ONNX", "Torch", "TensorRT"]
    for r in runtimes:
        fps = 30 + hash(r) % 15
        st.metric(label=f"{r} Inference FPS", value=f"{fps} FPS")

with tabs[9]:
    st.header("❤️ Health Check")
    st.markdown("Checking files, modules, and dependencies...")
    try:
        result = subprocess.run(["python", "tools/health_check.py"], capture_output=True, text=True)
        st.code(result.stdout if result.stdout else "No output", language='bash')
        if result.stderr:
            st.error(result.stderr)
    except Exception as e:
        st.error(str(e))