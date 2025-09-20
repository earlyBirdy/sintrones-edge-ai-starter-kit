import os, sqlite3, pandas as pd, streamlit as st
DB = os.getenv("EDGE_DB_PATH","data/edge.db")
con = sqlite3.connect(DB)
st.caption(f"DB: {os.path.abspath(DB)}")

st.header("🧰 Triage Queue (triage_queue)")
tri = pd.read_sql_query("""
  SELECT id, ts, unit_id, device_id, station, defect, score, assignee, sla_hours, status, notes
  FROM triage_queue ORDER BY ts DESC
""", con)
st.dataframe(tri, width='stretch')

st.header("📊 Benchmark Matrix (benchmark_results)")
bench = pd.read_sql_query("""
  SELECT device_id, model_id, model_ver, engine, input_size, fps, latency_ms, f1, ts
  FROM benchmark_results
  WHERE device_id='dev-A' AND model_id='defect-detector' AND model_ver='1.0.0' AND input_size=640
  ORDER BY ts
""", con)
st.dataframe(bench, width='stretch')
