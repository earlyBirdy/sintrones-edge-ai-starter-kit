import streamlit as st
import pandas as pd
from pathlib import Path
def render_mes_export():
    st.subheader("📤 MES Export")
    csv = Path("mes_latest.csv")
    if not csv.exists():
        st.info("Put a 'mes_latest.csv' in the repo root to preview/export.")
        return
    try:
        df = pd.read_csv(csv)
    except Exception as e:
        st.error(f"Failed to read {csv}: {e}")
        return
    st.dataframe(df, use_container_width=True)
    st.download_button("Download CSV", csv.read_bytes(), file_name=csv.name)