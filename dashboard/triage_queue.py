
import streamlit as st
import json
from pathlib import Path
from quality.triage import build_queue_from_anomalies, save_queue

def _rule_preview(rec):
    # Very simple preview payload
    return {
        "if": {"label": rec.get("label", "NG-defect1"), "min_score": rec.get("score", 0.8)},
        "then": {"action": "alert_and_log"}
    }

def render_triage_queue():
    st.subheader("🧰 Triage Queue")
    queue = build_queue_from_anomalies()
    if not queue:
        return st.info("No anomalies in ./logs/anomalies — drop images there to triage.")
    ids = [r["id"] for r in queue]
    sel = st.selectbox("Select item", ids)
    rec = next(r for r in queue if r["id"] == sel)

    # Show image if present
    img_path = rec.get("path")
    st.write(f"**ID:** {rec['id']}  •  **Score:** {rec.get('score')}")
    if img_path and Path(img_path).exists():
        st.image(img_path, caption=img_path)

    label = st.selectbox("Label", ["OK","NG-defect1","NG-defect2"], index=1 if rec.get("label") in (None,"") else (["OK","NG-defect1","NG-defect2"].index(rec.get("label")) if rec.get("label") in ["OK","NG-defect1","NG-defect2"] else 1))
    notes = st.text_area("Notes", rec.get("notes",""))

    c1, c2, c3 = st.columns(3)
    if c1.button("Save Label/Notes"):
        rec["label"] = label
        rec["notes"] = notes
        save_queue(queue)
        st.success("Saved")
    if c2.button("Promote → Rule"):
        st.success(f"Rule preview: {json.dumps(_rule_preview(rec))}")
    if c3.button("Refresh Queue"):
        st.rerun()
