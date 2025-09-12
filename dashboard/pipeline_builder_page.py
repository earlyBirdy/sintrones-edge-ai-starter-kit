import os, yaml, streamlit as st

PIPELINE_PATH = "recipes/pipeline.yaml"

def render_pipeline_builder():
    st.subheader("🧱 Pipeline Builder")
    st.caption("Compose: Pre-proc → Model → Post-proc → Rules → Outputs (I/O). Export to recipes/pipeline.yaml")

    # Pre-processing
    with st.expander("Pre-processing"):
        resize = st.selectbox("Resize", ["none", "320", "480", "640", "960"], index=3)
        normalize = st.checkbox("Normalize (mean/std)", value=True)
        denoise = st.checkbox("Denoise", value=False)

    # Model
    with st.expander("Model"):
        model_id = st.text_input("Model ID", "defect-detector")
        model_version = st.text_input("Model Version", "1.2.0")
        runtime = st.selectbox("Runtime", ["auto","onnxruntime","openvino","tensorrt"], index=0)
        confidence = st.slider("Confidence threshold", 0.0, 1.0, 0.5, 0.01)

    # Post-processing
    with st.expander("Post-processing"):
        nms = st.checkbox("NMS (object detection)", value=True)
        topk = st.number_input("Top-K", min_value=1, max_value=200, value=100)

    # Rules binding
    with st.expander("Rules"):
        attach_rules = st.checkbox("Attach rules from recipes/rules/*.yaml", value=True)

    # Outputs (I/O)
    with st.expander("Outputs / I/O"):
        emit_pass_fail = st.checkbox("Emit PASS/FAIL to connectors", value=True)
        save_artifacts = st.checkbox("Save crops/overlays to logs/", value=True)

    # Persist
    if st.button("Export pipeline.yaml"):
        cfg = {
            "preprocess": {"resize": None if resize=="none" else int(resize), "normalize": bool(normalize), "denoise": bool(denoise)},
            "model": {"id": model_id, "version": model_version, "runtime": runtime, "confidence": float(confidence)},
            "postprocess": {"nms": bool(nms), "topk": int(topk)},
            "rules": {"attach_repo_rules": bool(attach_rules)},
            "outputs": {"emit_pass_fail": bool(emit_pass_fail), "save_artifacts": bool(save_artifacts)},
        }
        os.makedirs(os.path.dirname(PIPELINE_PATH), exist_ok=True)
        with open(PIPELINE_PATH, "w", encoding="utf-8") as f:
            yaml.safe_dump(cfg, f, sort_keys=False)
        st.success(f"Exported {PIPELINE_PATH}")
