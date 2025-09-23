import streamlit as st, os
from pathlib import Path
def render_health_check():
    st.subheader("🧪 Health Check")
    db = Path(os.getenv("EDGE_DB_PATH") or (Path.cwd()/ "data" / "edgekit.db"))
    st.write(f"DB path: {db}")
    st.info("Stub page. Extend with DB checks.")