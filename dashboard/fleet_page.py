import streamlit as st
from fleet.fleet_registry import list_devices, heartbeat, set_active_pack, raise_alarm
def render_fleet_page():
    st.subheader("🛰️ Fleet")
    devs=list_devices()
    try: st.dataframe(devs, width='stretch')
    except Exception: st.write(devs)
    device=st.selectbox("Device",[d["id"] for d in devs]) if devs else None
    if not device: st.info("No devices yet."); return
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("Heartbeat"): heartbeat(device); st.success("Heartbeat sent")
    with c2:
        new_pack=st.text_input("Set Active Pack","")
        if st.button("Apply Pack"): set_active_pack(device,new_pack); st.success("Pack set")
    with c3:
        alarm=st.text_input("Raise Alarm","")
        if st.button("Send Alarm"): raise_alarm(device,alarm); st.warning("Alarm raised")
