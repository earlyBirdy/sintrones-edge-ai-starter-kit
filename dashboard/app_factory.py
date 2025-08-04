import streamlit as st
import random

st.set_page_config(page_title="Factory Monitoring Dashboard")
st.title("🏭 Factory Edge AI Dashboard")

temperature = round(random.uniform(60, 90), 2)
vibration = round(random.uniform(0.01, 0.2), 3)

st.metric("Temperature (°C)", temperature)
st.metric("Vibration (g)", vibration)

if temperature > 75:
    st.warning("⚠️ Temperature exceeds safe limits!")
if vibration > 0.15:
    st.warning("⚠️ High vibration detected!")
