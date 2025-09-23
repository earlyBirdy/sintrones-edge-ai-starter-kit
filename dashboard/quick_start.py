import streamlit as st
import pandas as pd
from pathlib import Path
from .ui_utils import connect, table_exists

def render_quick_start():
    st.title("🏁 Quick Start")
    st.caption("End-to-end snapshot of your Edge AI kit — devices, events, inspections, and exports.")

    con = connect()
    counts = {}
    for t in ["devices","inspections","events","benchmarks","anomalies"]:
        counts[t] = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] if table_exists(con, t) else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Devices", counts["devices"])
    c2.metric("Inspections", counts["inspections"])
    c3.metric("Events (24h)", counts["events"])
    c4.metric("Benchmarks", counts["benchmarks"])
    c5.metric("Anomalies", counts["anomalies"])

    st.divider()
    st.subheader("Recent Activity")
    # last 50 inspections
    if table_exists(con,"inspections"):
        df = pd.read_sql_query("SELECT ts, unit_id, result, score FROM inspections ORDER BY ts DESC LIMIT 50", con)
        st.dataframe(df, width='stretch', height=260)
    else:
        st.info("No `inspections` table yet.")

    st.subheader("Latest Events")
    if table_exists(con,"events"):
        df = pd.read_sql_query("SELECT ts, device_id, type, message FROM events ORDER BY ts DESC LIMIT 50", con)
        st.dataframe(df, width='stretch', height=240)
    else:
        st.info("No `events` table yet.")

    st.subheader("Fast Links")
    st.write("- 📁 Open logs folder: `./logs/`")
    st.write("- 📤 Latest MES export: `mes_latest.csv`")
