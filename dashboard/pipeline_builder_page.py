import streamlit as st
from pipeline.pipeline_builder import export_pipeline

def render_pipeline_builder():
    st.subheader("🧱 Pipeline Builder")
    if st.button("Export Minimal Pipeline"):
        p = export_pipeline()
        st.success(f"Exported to {p}")
