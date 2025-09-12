import os, yaml, json, streamlit as st, time
CFG_PATH="connectors/config.yaml"
def _load_cfg():
    if os.path.exists(CFG_PATH):
        with open(CFG_PATH,"r",encoding="utf-8") as f: return yaml.safe_load(f) or {}
    return {"cameras": [], "opcua": {}, "modbus": {}, "mqtt": {}}
def _save_cfg(cfg):
    os.makedirs(os.path.dirname(CFG_PATH), exist_ok=True)
    with open(CFG_PATH,"w",encoding="utf-8") as f: yaml.safe_dump(cfg,f,sort_keys=False)
def render_io_connectors():
    st.subheader("⚙️ I/O Connectors")
    cfg=_load_cfg()
    st.markdown("### Cameras")
    with st.expander("Add Camera"):
        name=st.text_input("Name","cam-1")
        kind=st.selectbox("Type",["USB","RTSP","GigE"])
        uri=st.text_input("URI / Device","/dev/video0" if kind=="USB" else "rtsp://...")
        if st.button("Add Camera"):
            cfg.setdefault("cameras", []).append({"name":name,"type":kind,"uri":uri}); _save_cfg(cfg); st.success("Camera added")
    if cfg.get("cameras"): st.table(cfg["cameras"])
    st.markdown("### PLC / Fieldbus")
    opc_host=st.text_input("OPC-UA endpoint", cfg.get("opcua",{}).get("endpoint","opc.tcp://localhost:4840"))
    modbus_host=st.text_input("Modbus/TCP host", cfg.get("modbus",{}).get("host","127.0.0.1"))
    modbus_port=st.number_input("Modbus/TCP port", 1, 65535, int(cfg.get("modbus",{}).get("port",502)))
    if st.button("Save PLC settings"):
        cfg["opcua"]={"endpoint":opc_host}; cfg["modbus"]={"host":modbus_host,"port":int(modbus_port)}; _save_cfg(cfg); st.success("Saved PLC settings")
    st.markdown("### MQTT (to MES)")
    mqtt_host=st.text_input("MQTT host", cfg.get("mqtt",{}).get("host","localhost"))
    mqtt_topic=st.text_input("MQTT topic", cfg.get("mqtt",{}).get("topic","edge/results"))
    if st.button("Save MQTT"):
        cfg["mqtt"]={"host":mqtt_host,"topic":mqtt_topic}; _save_cfg(cfg); st.success("Saved MQTT")
    st.divider(); st.markdown("#### Dry-run: emit a PASS/FAIL event (simulation)")
    unit=st.text_input("Unit ID","U-0001"); result=st.selectbox("Result",["PASS","FAIL"])
    if st.button("Simulate Emit"):
        os.makedirs("logs", exist_ok=True)
        line={"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "unit_id": unit, "result": result, "source": "io_sim"}
        with open("logs/events.jsonl","a",encoding="utf-8") as f: f.write(json.dumps(line)+"\n")
        st.success("Emitted to logs/events.jsonl (simulation)")
