import os
import streamlit as st

def show_log_viewer(show_title: bool = True):
    if show_title:
        st.subheader("📁 Anomaly Log Viewer")
    log_dir = os.path.join("logs", "anomalies")
    if not os.path.isdir(log_dir):
        st.info("No anomaly logs found in ./logs/anomalies")
        return
    images = [f for f in sorted(os.listdir(log_dir)) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    if not images:
        st.info("No images found in ./logs/anomalies")
        return
    cols = st.columns(3)
    for i, fn in enumerate(images):
        path = os.path.join(log_dir, fn)
        with cols[i % 3]:
            st.image(path, caption=fn, use_column_width=True)
