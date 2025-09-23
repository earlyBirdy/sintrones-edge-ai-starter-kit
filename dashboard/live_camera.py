import streamlit as st, yaml
from pathlib import Path

def render_live_camera():
    st.title("🎥 Live Camera Feed")
    st.caption("Lists configured camera endpoints. For RTSP/HTTP preview, integrate your player.")
    cfg = Path("config/cameras.yaml")
    if not cfg.exists():
        st.info("Add your cameras in `config/cameras.yaml`")
        st.code("cameras:\n  - id: cam0\n    url: rtsp://...")
        return
    cams = yaml.safe_load(cfg.read_text()) or {}
    for cam in cams.get("cameras", []):
        with st.container(border=True):
            st.subheader(cam.get("id","cam"))
            st.code(cam.get("url",""))
            st.write("Preview: (integrate OpenCV/RTSP client as needed)")
