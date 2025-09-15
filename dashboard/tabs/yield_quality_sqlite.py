import pandas as pd, streamlit as st
from core.db import connect

def render_yield_quality_sqlite():
    st.header('Yield & Quality', anchor=False)
    con = connect()
    df = pd.read_sql_query("""SELECT date(ts) as day,
             SUM(result='PASS') as pass_cnt,
             SUM(result='FAIL') as fail_cnt
      FROM inspections GROUP BY date(ts) ORDER BY day DESC LIMIT 30""", con)
    if df.empty:
        st.info('No inspection data yet.')
        return
    df['yield_%'] = (df['pass_cnt'] / (df['pass_cnt'] + df['fail_cnt']).clip(lower=1))*100
    st.line_chart(df.set_index('day')[['yield_%']])
    st.dataframe(df, width='stretch')
