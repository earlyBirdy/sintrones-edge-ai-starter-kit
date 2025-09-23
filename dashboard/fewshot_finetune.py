import streamlit as st
from pathlib import Path

def render_fewshot():
    st.title("🛠️ Few‑Shot Fine‑Tuning")
    root = Path("models/fewshot")
    root.mkdir(parents=True, exist_ok=True)
    st.caption("Drop few‑shot examples here. This UI lists files and shows a simple spec.")
    files = sorted([p for p in root.glob("**/*") if p.is_file()])
    if not files:
        st.info("Put example images/JSON in `models/fewshot/`")
    else:
        for p in files[:200]:
            st.write("•", p.as_posix())
    st.subheader("Spec (example)")
    st.code("""{
  "engine": "yolo-v8.2",
  "shots": 8,
  "classes": ["scratch","misalign"],
  "epochs": 5
}""")
