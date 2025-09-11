import streamlit as st
from io_connectors.industrial_io import opcua_status, modbus_status, mqtt_status

def render_io_connectors():
    st.subheader("⚙️ I/O Connectors")
    st.json({"OPC-UA":opcua_status(), "Modbus":modbus_status(), "MQTT":mqtt_status()})
