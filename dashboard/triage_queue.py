import streamlit as st
from quality.triage import build_queue_from_anomalies, save_queue
from rules.rules_engine import promote_to_rule
def render_triage_queue():
    st.subheader("🧰 Triage Queue")
    q=build_queue_from_anomalies()
    if not q: return st.info("No anomalies in ./logs/anomalies")
    ids=[r["id"] for r in q]; sel=st.selectbox("Select", ids); rec=next(r for r in q if r["id"]==sel)
    st.image(rec["path"], caption=f"{rec['id']} (score={rec['score']})")
    label=st.selectbox("Label",["OK","NG-defect1","NG-defect2"], index=1); notes=st.text_area("Notes","")
    c1,c2,c3=st.columns(3)
    if c1.button("Save Label/Notes"): rec["label"]=label; rec["notes"]=notes; save_queue(q); st.success("Saved")
    if c2.button("Promote → Rule"): st.success(f"Rule created: {promote_to_rule(rec, roi={'x':0,'y':0,'w':100,'h':100}, threshold=0.85)}")
    if c3.button("Refresh Queue"): st.experimental_rerun()
