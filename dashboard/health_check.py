import streamlit as st
import pandas as pd
import sqlite3, os
from pathlib import Path
from .ui_utils import connect, table_exists, DB_PATH

def render_health_check():
    st.title("🧪 Health Check")
    st.caption(f"DB path: `{DB_PATH}`")

    con = connect()
    checks = []
    for t in ["devices","sensor_readings","inspections","events","benchmarks","anomalies","event_log"]:
        ok = table_exists(con, t)
        cnt = None
        if ok:
            try:
                cnt = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            except Exception as e:
                cnt = f"ERR: {e}"
        checks.append({"table": t, "exists": ok, "rows": cnt})
    st.dataframe(pd.DataFrame(checks), width='stretch', height=320)

    # Filesystem checks
    fs = []
    for p in ["logs","logs/anomalies","mes_latest.csv","config/inspection_rules.yaml","config/cameras.yaml","config/policy.yaml","config/connectors","pipelines","xai_results","benchmarks","examples","models/packs","models/finetune","models/fewshot"]:
        path = Path(p)
        fs.append({"path": p, "exists": path.exists(), "type": "dir" if path.is_dir() else "file"})
    st.dataframe(pd.DataFrame(fs), width='stretch', height=320)
