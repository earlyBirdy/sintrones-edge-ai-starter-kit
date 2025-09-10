
import os, sys, json, subprocess
import streamlit as st

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT_DIR)

# ---- Imports with graceful fallbacks ----
try:
    from ai_workflow.inference_kit import run_inference as _run_inference
except Exception:
    _run_inference = None

try:
    from ai_workflow.trainer import log_training_progress
except Exception:
    log_training_progress = None

try:
    from multi_camera_support.multi_cam_streamer import get_mock_camera_feeds
except Exception:
    get_mock_camera_feeds = None

try:
    from xai_utils import saliency as xai_saliency
except Exception:
    xai_saliency = None
try:
    from xai_utils.saliency_map import generate_saliency
except Exception:
    generate_saliency = None

try:
    from dashboard.log_viewer import show_log_viewer
except Exception:
    show_log_viewer = None

try:
    from dashboard.benchmark_viewer import show_benchmark_viewer
except Exception:
    show_benchmark_viewer = None

try:
    from dashboard.status_panel import show_status_panel
except Exception:
    show_status_panel = None

# ---- Page Config ----
st.set_page_config(page_title="Sintrones Edge AI Dashboard", layout="wide")
st.title("🧠 Sintrones Edge AI Dashboard")

# ---- Tabs (AI-first) ----
tabs = st.tabs([
    "🏁 Quick Start", "🔍 Inference", "🎥 Live Camera Feed", "📷 Multi-Cam Feeds",
    "📁 Log Viewer", "📊 Benchmarking", "❤️ OTA/System Status", "🧪 Health Check",
    "📜 Data Traceability", "🧠 Train Model", "🔥 Saliency / XAI", "🛠️ Few-Shot Fine-Tuning", "📂 Examples"
])

# ---- 0) Quick Start ----
with tabs[0]:
    st.subheader("🏁 Quick Start")
    st.write("Prioritizes AI monitoring. Use tabs to run inference, preview cameras, view logs, check health, and manage traceability.")

# ---- 1) Inference ----
with tabs[1]:
    st.subheader("🔍 Inference")
    model_path = st.text_input("Model path", "models/defect_detector.onnx")
    img = st.file_uploader("Upload an image", type=["jpg","jpeg","png"])
    if st.button("Run Inference"):
        if _run_inference is None:
            st.warning("Inference module not found: ai_workflow/inference_kit.py")
        else:
            if img is None:
                st.error("Please upload an image first.")
            else:
                tmp_path = os.path.join("logs", "tmp")
                os.makedirs(tmp_path, exist_ok=True)
                img_path = os.path.join(tmp_path, img.name)
                with open(img_path, "wb") as f:
                    f.write(img.getbuffer())
                try:
                    result = _run_inference(model_path, img_path)
                    st.success(f"Result: {result}")
                except Exception as e:
                    st.exception(e)

# ---- 2) Live Camera Feed ----
with tabs[2]:
    st.subheader("🎥 Live Camera Feed")
    st.info("Connect a real camera in your own script, or use the Multi-Cam tab for mock feeds.")

# ---- 3) Multi-Cam Feeds ----
with tabs[3]:
    st.subheader("📷 Multi-Cam Feeds")
    if get_mock_camera_feeds is None:
        st.warning("multi_camera_support/multi_cam_streamer.py missing.")
    else:
        for p in get_mock_camera_feeds():
            if os.path.exists(p):
                st.image(p, caption=os.path.basename(p))
            else:
                st.write(f"Missing: {p}")

# ---- 4) Log Viewer ----
with tabs[4]:
    st.subheader("📁 Anomaly Log Viewer")
    if show_log_viewer:
        show_log_viewer()
    else:
        st.warning("dashboard/log_viewer.py missing.")

# ---- 5) Benchmarking ----
with tabs[5]:
    st.subheader("📊 Model Benchmark Panel")
    if show_benchmark_viewer:
        show_benchmark_viewer()
    else:
        st.warning("dashboard/benchmark_viewer.py missing.")

# ---- 6) OTA / System Status ----
with tabs[6]:
    st.subheader("❤️ OTA / System Status")
    if show_status_panel:
        show_status_panel()
    else:
        st.warning("dashboard/status_panel.py missing.")

# ---- 7) Health Check ----
with tabs[7]:
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

# ---- 8) Data Traceability (wired) ----
with tabs[8]:
    st.subheader("📜 Data Traceability")
    try:
        from data_traceability.traceability_indexer import build_trace_index, summarize_trace_index
        df = build_trace_index(log_root=os.path.join(ROOT_DIR, "logs"))
        if df is None or df.empty:
            st.info("No traceability records found under ./logs. Drop anomaly images into logs/anomalies or JSONL into logs/.")
        else:
            summary = summarize_trace_index(df)
            k1, k2, k3 = st.columns(3)
            k1.metric("Total Records", summary["total_records"])
            k2.metric("Anomaly Images", summary["anomaly_images"])
            k3.metric("JSON Events", summary["json_events"])

            st.markdown("#### Records")
            st.dataframe(df.fillna(""), use_container_width=True)
            if summary.get("labels"):
                st.markdown("#### Labels")
                st.json(summary["labels"])
            if summary.get("results"):
                st.markdown("#### Results")
                st.json(summary["results"])
            csv_bytes = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV", data=csv_bytes, file_name="traceability_index.csv", mime="text/csv")
    except Exception as e:
        st.exception(e)

# ---- 9) Train Model ----
with tabs[9]:
    st.subheader("🧠 Train Model")
    if log_training_progress is None:
        st.warning("ai_workflow/trainer.py missing or incomplete.")
    else:
        if st.button("Simulate Training"):
            metrics = {"loss": 0.12, "accuracy": 0.93}
            try:
                log_training_progress(metrics)
                st.success("Training metrics logged to logs/training/*.log")
            except Exception as e:
                st.exception(e)

# ---- 10) Saliency / XAI ----
with tabs[10]:
    st.subheader("🔥 Saliency / XAI")
    uploaded = st.file_uploader("Upload image for saliency", type=["jpg","jpeg","png"], key="sal")
    if st.button("Generate Saliency Map"):
        if uploaded is None:
            st.error("Upload an image first.")
        else:
            tmp_dir = os.path.join("logs","saliency")
            os.makedirs(tmp_dir, exist_ok=True)
            in_path = os.path.join(tmp_dir, uploaded.name)
            with open(in_path,"wb") as f: f.write(uploaded.getbuffer())
            if xai_saliency is not None:
                try:
                    import cv2, numpy as np
                    file_bytes = np.asarray(bytearray(uploaded.read()), dtype=np.uint8)
                    img_bgr = cv2.imdecode(file_bytes, 1)
                    out_path = os.path.join(tmp_dir, "saliency.jpg")
                    xai_saliency.save_saliency_map(img_bgr, out_path)
                    st.image(out_path, caption="Saliency Map")
                except Exception as e:
                    st.warning(f"OpenCV path failed: {e}")
                    if generate_saliency:
                        tag = generate_saliency(in_path)
                        st.write(f"Generated tag: {tag}")
            elif generate_saliency is not None:
                tag = generate_saliency(in_path)
                st.write(f"Generated tag: {tag}")
            else:
                st.warning("No XAI utilities available.")

# ---- 11) Few-Shot Fine-Tuning ----
with tabs[11]:
    st.subheader("🛠️ Few-Shot Fine-Tuning")
    st.info("Label a few anomaly frames, then export an ONNX update template.")
    up = st.file_uploader("Upload anomaly image", type=["jpg","jpeg","png"], key="ft")
    if up:
        st.image(up)
        label = st.selectbox("Label as:", ["OK", "NG-Defect1", "NG-Defect2"])
        st.success(f"Labeled: {label} (would save to template for ONNX)")

# ---- 12) Examples ----
with tabs[12]:
    st.subheader("📂 Examples")
    st.write("Example scripts detected under /examples:")
    examples = []
    for r, _, fs in os.walk(os.path.join(ROOT_DIR,"examples")):
        for f in fs:
            if f.endswith(".py"):
                examples.append(os.path.relpath(os.path.join(r,f), ROOT_DIR))
    if examples:
        for e in sorted(examples):
            st.code(f"python {e}")
    else:
        st.info("No examples found.")
