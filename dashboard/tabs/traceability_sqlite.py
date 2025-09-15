import pandas as pd, streamlit as st
from core.db import connect, migrate

def render_traceability_sqlite():
    st.header('Data Traceability', anchor=False)
    con = connect(); migrate(con)
    station = st.selectbox('Station', ['All','ST01','ST02'], index=0)
    result  = st.selectbox('Result', ['All','PASS','FAIL'], index=0)
    q = "SELECT ts, unit_id, station, result, model_pack||'@'||model_ver AS model, image_path FROM inspections WHERE 1=1"
    args = []
    if station!='All': q += ' AND station=?'; args.append(station)
    if result!='All':  q += ' AND result=?';  args.append(result)
    q += ' ORDER BY ts DESC LIMIT 500'
    df = pd.read_sql_query(q, con, params=args)
    st.dataframe(df, width='stretch')
