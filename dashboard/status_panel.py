import streamlit as st

def show_status_panel():
    st.subheader("⚙ OTA / System Status Panel")
    st.metric(label="Last OTA Update", value="2025-09-01 10:42")
    st.metric(label="Device Uptime", value="48h 12m")
    st.metric(label="Failed Inferences", value=2)