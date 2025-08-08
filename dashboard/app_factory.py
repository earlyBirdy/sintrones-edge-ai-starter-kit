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

# add at bottom of app_factory.py
def launch_dashboard():
    # This file is meant to be run via: streamlit run dashboard/app_factory.py
    # Calling this function from a normal python process won’t start Streamlit.
    import subprocess, sys
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__], check=True)

if __name__ == "__main__":
    # Running directly with: streamlit run dashboard/app_factory.py
    pass
