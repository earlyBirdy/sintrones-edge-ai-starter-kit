import pandas as pd, streamlit as st
from core.db import connect

def render_fleet_sqlite():
    st.header('Fleet', anchor=False)
    con = connect()
    st.subheader('Devices'); st.dataframe(pd.read_sql_query('SELECT * FROM devices', con), width='stretch')
    st.subheader('Recent Deployments'); st.dataframe(pd.read_sql_query('SELECT * FROM deployments ORDER BY deployed_at DESC LIMIT 100', con), width='stretch')
    st.subheader('Alarms / Events (24h)'); st.dataframe(pd.read_sql_query("SELECT * FROM events WHERE ts >= datetime('now','-24 hours') ORDER BY ts DESC", con), width='stretch')
