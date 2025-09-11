import streamlit as st
from quality.triage import build_queue_from_anomalies, save_queue, promote_to_rule

def render_triage_queue():
    st.subheader("🧰 Triage Queue")
    q = build_queue_from_anomalies()
    if not q:
        return st.info("No anomalies found in logs/anomalies")
    ids = [r["id"] for r in q]
    sel = st.selectbox("Select", ids)
    rec = next(r for r in q if r["id"]==sel)
    st.image(rec["path"], caption=rec["id"])
    label = st.selectbox("Label", ["OK","NG-defect1","NG-defect2"], index=1)
    c1,c2 = st.columns(2)
    if c1.button("Promote → Rule"):
        rule = promote_to_rule(rec, roi={"x":0,"y":0,"w":100,"h":100}, threshold=0.85)
        st.success(f"Rule created: {rule}")
    if c2.button("Save Queue"):
        save_queue(q)
        st.success("Queue saved.")
