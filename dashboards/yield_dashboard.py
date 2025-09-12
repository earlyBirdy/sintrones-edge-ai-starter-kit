import streamlit as st, pandas as pd
from data_traceability.traceability_indexer import build_trace_index
def _compute_metrics(df: pd.DataFrame):
    total=len(df)
    passes=int((df.get("result")=="PASS").sum()) if "result" in df.columns else 0
    fails=int((df.get("result")=="FAIL").sum()) if "result" in df.columns else 0
    yield_pct=(passes/max(1,passes+fails))*100.0
    ppm=(fails/max(1,total))*1_000_000.0
    labeled=int(df.get("has_label").sum()) if "has_label" in df.columns else 0
    return dict(total=total,passes=passes,fails=fails,yield_pct=yield_pct,ppm=ppm,labeled=labeled)
def _pareto(df: pd.DataFrame):
    if "defect" in df.columns and df["defect"].notna().any():
        series=df["defect"].fillna("unknown")
    else:
        if "label" in df.columns: series=df["label"].fillna("OK").apply(lambda x: x if str(x).startswith("NG") else "OK")
        else: series=pd.Series([], dtype=str)
    return series.value_counts().reset_index(names=["count"]).rename(columns={"index":"category"})
def render_yield_dashboard():
    st.subheader("📈 Yield & Quality")
    df=build_trace_index("logs")
    if df.empty:
        st.info("No trace data found. Put events/images under ./logs."); return
    with st.expander("Filters"):
        station=st.multiselect("Station", sorted([s for s in df.get("station_id", pd.Series([])).dropna().unique()]))
        shift=st.multiselect("Shift", sorted([s for s in df.get("shift", pd.Series([])).dropna().unique()]))
        vendor=st.multiselect("Vendor", sorted([s for s in df.get("vendor", pd.Series([])).dropna().unique()]))
        modelv=st.multiselect("Model Version", sorted([s for s in df.get("model_version", pd.Series([])).dropna().unique()]))
        if station: df=df[df["station_id"].isin(station)]
        if shift: df=df[df["shift"].isin(shift)]
        if vendor: df=df[df["vendor"].isin(vendor)]
        if modelv: df=df[df["model_version"].isin(modelv)]
    m=_compute_metrics(df)
    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("Total", m["total"]); c2.metric("PASS", m["passes"]); c3.metric("FAIL", m["fails"])
    c4.metric("Yield %", f"{m['yield_pct']:.2f}%"); c5.metric("DPPM", f"{m['ppm']:.0f}")
    if "day" in df.columns and df["day"].notna().any():
        trend=df.groupby("day").apply(lambda g: (g["result"]=="FAIL").sum()).reset_index(name="fails")
        trend["yield_pct"]=df.groupby("day").apply(lambda g: ((g["result"]=="PASS").sum()/max(1,((g["result"]=="PASS").sum()+(g["result"]=="FAIL").sum())))*100.0).values
        st.line_chart(trend.set_index("day")[["fails","yield_pct"]])
    pareto=_pareto(df).head(15)
    if not pareto.empty: st.bar_chart(pareto.set_index("category")["count"])
    else: st.info("No defect categories found to plot Pareto.")
