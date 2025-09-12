import streamlit as st
import pandas as pd
from data_traceability.traceability_indexer import build_trace_index

def render_traceability_page():
    st.subheader("📜 Data Traceability")
    df = build_trace_index("logs")
    if df.empty:
        st.info("No trace data found. Generate logs or events under ./logs.")
        return

    total = len(df)
    labeled = int(df["has_label"].sum()) if "has_label" in df.columns else 0
    fails = int((df.get("result") == "FAIL").sum()) if "result" in df.columns else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Total records", total)
    c2.metric("Labeled", labeled)
    c3.metric("FAIL events", fails)

    with st.expander("Filters"):
        station = st.multiselect("Station", sorted([s for s in df.get("station_id", pd.Series([])).dropna().unique()]))
        model = st.multiselect("Model", sorted([s for s in df.get("model", pd.Series([])).dropna().unique()]))
        res = st.multiselect("Result", sorted([s for s in df.get("result", pd.Series([])).dropna().unique()]))
        if station:
            df = df[df["station_id"].isin(station)]
        if model:
            df = df[df["model"].isin(model)]
        if res:
            df = df[df["result"].isin(res)]

    st.dataframe(df, width='stretch')
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"),
                       "traceability.csv", "text/csv")
