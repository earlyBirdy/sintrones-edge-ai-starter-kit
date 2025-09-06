import streamlit as st
from dashboard.log_viewer import show_log_viewer
from dashboard.benchmark_viewer import show_benchmark_viewer
from dashboard.status_panel import show_status_panel

st.set_page_config(page_title="Edge AI Dashboard", layout="wide")
st.title("🧠 Sintrones Edge AI Dashboard")

# Show all panels
show_log_viewer()
show_benchmark_viewer()
show_status_panel()