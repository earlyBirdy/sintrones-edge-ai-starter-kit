import streamlit as st, pandas as pd
from rules.rules_engine import list_rules
def render_rules_page():
    st.subheader("✅ Inspection Rules")
    rules=list_rules()
    if rules:
        st.dataframe(pd.DataFrame(rules), width='stretch')
    else:
        st.info("No rules yet. Promote some from Triage.")
