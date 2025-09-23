import streamlit as st
import pandas as pd
from .ui_utils import connect, table_exists

def _cols(con, table):
    try:
        return [r[1] for r in con.execute(f"PRAGMA table_info({table});").fetchall()]
    except Exception:
        return []

def _best_table(con):
    return "traceability_view" if table_exists(con, "traceability_view") else ("inspections" if table_exists(con, "inspections") else None)

def render_traceability_sqlite():
    st.title("📇 Data Traceability")
    st.caption("Lot/Unit trace with adaptive columns (works even if your schema is minimal).")

    con = connect()
    table = _best_table(con)
    if not table:
        st.warning("No `traceability_view` or `inspections` found.")
        st.stop()

    with st.expander("Filters"):
        unit_like = st.text_input("Unit ID contains", "")
        only_fail = st.checkbox("Only FAIL", False)
        limit = st.slider("Rows", 50, 5000, 500, 50)

    cols = _cols(con, table)
    proj = []
    for c in ["ts","unit_id","station","result","score","sensor_id"]:
        if c in cols:
            proj.append(c)
        else:
            proj.append(f"NULL AS {c}")
    sql = f"SELECT {', '.join(proj)} FROM {table}"
    where = []
    params = []
    if unit_like and "unit_id" in cols:
        where.append("unit_id LIKE ?"); params.append(f"%{unit_like}%")
    if only_fail and "result" in cols:
        where.append("result='FAIL'")
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY ts DESC LIMIT ?"; params.append(limit)

    try:
        df = pd.read_sql_query(sql, con, params=params)
    except Exception as e:
        st.error(f"Traceability query failed: {e}")
        st.code(sql)
        return

    st.dataframe(df, width='stretch', height=520)
