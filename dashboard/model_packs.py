import streamlit as st
from orchestration.model_pack import load_model_pack, validate_pack, select_engine, deploy_pack

def render_model_packs_page():
    st.subheader("📦 Model Packs")
    pack_dir = st.text_input("Model Pack directory", "model_packs/defect-detector/1.2.0")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Validate"):
            pack = load_model_pack(pack_dir)
            issues = validate_pack(pack)
            if not issues: st.success("Pack valid ✅")
            else:
                for i in issues: st.warning(f"[{i.level}] {i.message}")
    with col2:
        if st.button("Select Engine"):
            pack = load_model_pack(pack_dir)
            engine = select_engine(pack, {"platform":"x86_64","accel":"cpu"})
            st.info(f"Selected runtime: {engine}")
    with col3:
        device = st.text_input("Device ID", "edge-01")
        if st.button("Deploy"):
            pack = load_model_pack(pack_dir)
            res = deploy_pack(pack, device)
            st.success(f"Deployed: {res}")
