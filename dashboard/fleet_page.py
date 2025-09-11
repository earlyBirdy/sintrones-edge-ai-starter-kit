import streamlit as st
from fleet.fleet_registry import list_devices

def render_fleet_page():
    st.subheader("🛰️ Fleet")
    devs = list_devices()
    st.dataframe(devs, use_container_width=True)
