import os, yaml, json, hashlib, streamlit as st

def _load_modelpack(pack_dir: str):
    y = os.path.join(pack_dir, "modelpack.yaml")
    if os.path.exists(y):
        with open(y,"r",encoding="utf-8") as f: return yaml.safe_load(f) or {}
    return {}

def _artifact_sha256(path: str):
    if not os.path.exists(path): return ""
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda: f.read(65536), b""): h.update(c)
    return h.hexdigest()

def render_governance():
    st.subheader("🔐 Data & Model Governance")
    pack_dir = st.text_input("Model Pack directory", "model_packs/defect-detector/1.2.0")
    pack = _load_modelpack(pack_dir)
    if not pack:
        st.info("No modelpack.yaml found.")
        return

    st.markdown("### Lineage")
    st.json({
        "model_id": pack.get("model_id"),
        "version": pack.get("version"),
        "train_data_commit": pack.get("train",{}).get("data_commit"),
        "metrics": pack.get("metrics",{}),
        "benchmarks": pack.get("benchmarks",{})
    })

    st.markdown("### Sign / Verify Artifacts")
    arts = pack.get("artifacts", {})
    rows = []
    for name, rel in (arts or {}).items():
        p = os.path.join(pack_dir, rel)
        rows.append({"name": name, "path": p, "exists": os.path.exists(p), "sha256": _artifact_sha256(p)})
    if rows:
        st.dataframe(rows, width='stretch')

    sig_path = os.path.join(pack_dir, "SIGNATURES.json")
    if st.button("Write SIGNATURES.json"):
        with open(sig_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, indent=2)
        st.success(f"Wrote {sig_path}")

    st.markdown("### DVC / Git-LFS status (manual)")
    st.caption("Run these in your repo root; paste outputs here for record:")
    st.code("dvc status\n
git lfs ls-files", language="bash")
