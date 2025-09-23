import streamlit as st
import pandas as pd
import sqlite3, os
from .ui_utils import connect, table_exists

CANON = ["ts","device_id","engine","input_path","output_path","score"]

def _cols(con, table):
    try:
        cur = con.execute(f"PRAGMA table_info({table});")
        return [r[1] for r in cur.fetchall()]
    except Exception:
        return []

def _build_select(table, cols_have):
    # pick the intersection, fill missing as NULL
    selects = []
    for c in CANON:
        if c in cols_have:
            selects.append(c)
        else:
            selects.append(f"NULL AS {c}")
    return f"SELECT {', '.join(selects)} FROM {table}"

def render_inference():
    st.title("🔍 Inference")
    st.caption("Adaptive view of inference events — works with legacy or custom schemas.")

    con = connect()
    # Prefer a normalized view if present
    use_table = None
    if table_exists(con, "inference_events_view"):
        use_table = "inference_events_view"
    elif table_exists(con, "inference_events"):
        use_table = "inference_events"
    else:
        st.info("No inference table found. Create `inference_events` or the compatibility view `inference_events_view`.")
        st.code("""-- Example compatibility view
CREATE VIEW IF NOT EXISTS inference_events_view AS
SELECT
  ts,
  device_id,
  NULL AS engine,
  NULL AS input_path,
  NULL AS output_path,
  NULL AS score
FROM sensor_readings;""")
        return

    with st.expander("Filters"):
        device = st.text_input("Device contains", "")
        engine = st.text_input("Engine contains (if available)", "")
        limit = st.slider("Rows", 50, 2000, 200, 50)

    cols_have = _cols(con, use_table)
    base = _build_select(use_table, cols_have)
    where = []
    params = []
    if device:
        where.append("device_id LIKE ?"); params.append(f"%{device}%")
    if engine and ("engine" in cols_have):
        where.append("engine LIKE ?"); params.append(f"%{engine}%")
    sql = base
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY ts DESC LIMIT ?"; params.append(limit)

    try:
        df = pd.read_sql_query(sql, con, params=params)
    except Exception as e:
        st.error(f"Query failed: {e}")
        st.code(sql)
        return

    if df.empty:
        st.info("No inference rows yet.")
        return

    st.dataframe(df, width='stretch', height=460)
    if "score" in df and df["score"].notna().any():
        st.line_chart(df.sort_values("ts")[["score"]], x="ts", width='stretch')
    else:
        st.caption("No numeric scores available to chart yet.")
