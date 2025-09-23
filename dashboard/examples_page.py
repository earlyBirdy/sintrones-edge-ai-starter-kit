import streamlit as st
from pathlib import Path

def render_examples():
    st.title("📂 Examples")
    root = Path("examples")
    root.mkdir(exist_ok=True)
    items = sorted([p for p in root.glob("**/*") if p.is_file()])
    if not items:
        st.info("Put your example notebooks, configs, or images into `examples/`.")
        return
    for p in items:
        with open(p, "rb") as f:
            st.download_button(f"Download {p.name}", data=f.read(), file_name=p.name)
