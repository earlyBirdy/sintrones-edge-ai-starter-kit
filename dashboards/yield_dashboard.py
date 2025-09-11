import streamlit as st
import pandas as pd

def render_yield_dashboard():
    st.subheader("📈 Yield & Quality")
    df = pd.DataFrame([
        {"date":"2025-09-10","yield_pct":98.7,"ppm":130},
        {"date":"2025-09-11","yield_pct":99.2,"ppm":80}
    ])
    st.dataframe(df, use_container_width=True)
