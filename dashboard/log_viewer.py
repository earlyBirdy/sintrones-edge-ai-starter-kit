import streamlit as st
import os

def show_log_viewer():
    st.subheader("📁 Anomaly Log Viewer")
    log_dir = "logs/anomalies"
    if os.path.exists(log_dir):
        for fname in os.listdir(log_dir):
            if fname.endswith(".jpg") or fname.endswith(".png"):
                st.image(os.path.join(log_dir, fname), caption=fname)
    else:
        st.info("No anomaly logs found.")