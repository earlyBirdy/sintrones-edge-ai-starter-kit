import streamlit as st
import random

st.set_page_config(page_title="Factory Automation Dashboard")

st.title("🏭 Factory Automation Monitoring")
st.subheader("Live Sensor Data")

# Simulated data
temp = random.uniform(60, 90)
vibration = random.uniform(0.01, 0.2)

st.metric("Temperature (°C)", f"{temp:.2f}")
st.metric("Vibration (g)", f"{vibration:.3f}")

if temp > 75:
    st.warning("⚠️ High temperature detected!")

if vibration > 0.15:
    st.warning("⚠️ Abnormal vibration detected!")
