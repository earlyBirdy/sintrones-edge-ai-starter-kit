import streamlit as st
from rules.rules_engine import list_rules

def render_rules_page():
    st.subheader("✅ Inspection Rules")
    st.dataframe(list_rules(), use_container_width=True)
