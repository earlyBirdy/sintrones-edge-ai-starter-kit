
import streamlit as st
import pandas as pd
import os
import glob
import json
from PIL import Image
import matplotlib.pyplot as plt

st.set_page_config(page_title="Edge AI Dashboard", layout="wide")

st.title("📊 Sintrones Edge AI Dashboard")

tabs = st.tabs(["✅ Anomaly Log Viewer", "📈 Model Benchmark Viewer", "🖼️ Heatmap Comparison", "⚙ OTA / System Status"])

# === Anomaly Log Viewer ===
with tabs[0]:
    st.header("✅ Anomaly Log Viewer")
    log_dir = "logs/"
    if os.path.exists(log_dir):
        log_files = glob.glob(os.path.join(log_dir, "*.csv"))
        if log_files:
            selected_log = st.selectbox("Select a log file", log_files)
            df = pd.read_csv(selected_log)
            st.dataframe(df)
        else:
            st.warning("No CSV log files found in logs/")
    else:
        st.warning("logs/ directory not found.")

# === Model Benchmark Viewer ===
with tabs[1]:
    st.header("📈 Model Benchmark Viewer")
    benchmark_file = "benchmarks/benchmark.json"
    if os.path.exists(benchmark_file):
        with open(benchmark_file, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        if all(col in df.columns for col in ['runtime', 'fps', 'latency_ms']):
            st.bar_chart(df.set_index("runtime")[["fps", "latency_ms"]])
        else:
            st.warning("benchmark.json is missing expected columns: 'runtime', 'fps', 'latency_ms'")
    else:
        st.info("No benchmark file found at benchmarks/benchmark.json")

# === Heatmap Comparison ===
with tabs[2]:
    st.header("🖼️ Heatmap Comparison")
    col1, col2 = st.columns(2)
    with col1:
        img1_path = st.text_input("Original Image Path", "samples/original.jpg")
        if os.path.exists(img1_path):
            st.image(img1_path, caption="Original", use_column_width=True)
        else:
            st.warning("Image not found.")
    with col2:
        heatmap_path = st.text_input("Heatmap Image Path", "samples/heatmap.jpg")
        if os.path.exists(heatmap_path):
            st.image(heatmap_path, caption="Heatmap", use_column_width=True)
        else:
            st.warning("Heatmap not found.")

# === OTA / System Status ===
with tabs[3]:
    st.header("⚙ OTA / System Status Panel")
    system_file = "system/status.json"
    if os.path.exists(system_file):
        with open(system_file, "r") as f:
            sys_info = json.load(f)
        st.json(sys_info)
    else:
        st.info("No status file found. Looking for system/status.json")
