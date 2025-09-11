import streamlit as st
from governance.model_lineage import get_lineage

def render_governance():
    st.subheader("🔐 Governance")
    st.dataframe(get_lineage(), use_container_width=True)
