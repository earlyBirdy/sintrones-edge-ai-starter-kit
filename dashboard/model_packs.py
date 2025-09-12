import streamlit as st
from orchestration.model_pack import load_model_pack, validate_pack, smoke_test, select_engine, persist_bench_result, deploy_pack, rollback
def render_model_packs_page():
    st.subheader("📦 Model Packs")
    pack_dir=st.text_input("Model Pack directory","model_packs/defect-detector/1.2.0")
    c1,c2,c3,c4=st.columns(4)
    with c1:
        if st.button("Validate"):
            pack=load_model_pack(pack_dir); issues=validate_pack(pack)
            if not issues: st.success("Pack valid ✅")
            else:
                for i in issues: getattr(st, "warning" if i["level"]!="error" else "error")(f"[{i['level']}] {i['message']}")
    with c2:
        if st.button("Smoke Test"): st.json(smoke_test(pack_dir))
    with c3:
        if st.button("Select Engine"):
            eng=select_engine(load_model_pack(pack_dir), {"platform":"x86_64","accel":"cpu"}); st.info(f"Selected: {eng}")
    with c4:
        device=st.text_input("Device ID","edge-01")
        d1,d2=st.columns(2)
        with d1:
            if st.button("Deploy"): st.success(deploy_pack(pack_dir, device))
        with d2:
            if st.button("Rollback"): st.warning(rollback(device))
    st.markdown("### Save Benchmark → modelpack.yaml")
    e=st.selectbox("Engine",["onnxruntime","openvino","tensorrt"]); s=st.selectbox("Size",["320","480","640","960"])
    fps=st.number_input("FPS",0.0,10000.0,30.0); lat=st.number_input("Latency (ms)",0.0,10000.0,33.0)
    if st.button("Save Benchmark"): persist_bench_result(pack_dir,e,s,fps,lat); st.success("Saved benchmark")
