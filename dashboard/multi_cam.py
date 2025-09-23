import streamlit as st, yaml
from pathlib import Path

def render_multi_cam():
    st.title("📷 Multi-Cam Feeds")
    cfg = Path("config/cameras.yaml")
    cams = []
    if cfg.exists():
        cams = (yaml.safe_load(cfg.read_text()) or {}).get("cameras", [])
    if not cams:
        st.info("No cameras defined. Add them in `config/cameras.yaml`.")
        return
    cols = st.columns(3)
    for i, cam in enumerate(cams):
        with cols[i % 3].container(border=True):
            st.subheader(cam.get("id","cam"))
            st.code(cam.get("url",""))
            st.write("Preview here (placeholder).")
