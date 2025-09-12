import streamlit as st, pandas as pd
from bench.benchmark_matrix import run_matrix
from orchestration.model_pack import persist_bench_result

def render_benchmark_matrix():
    st.subheader("📊 Benchmark Matrix")
    sizes = st.multiselect("Input sizes", ["320", "480", "640", "960"], default=["640", "960"])
    engines = st.multiselect("Engines", ["onnxruntime", "openvino", "tensorrt"], default=["onnxruntime", "tensorrt"])
    pack_dir = st.text_input("Persist into Model Pack", "model_packs/defect-detector/1.2.0")
    if st.button("Run Matrix"):
        data = run_matrix(sizes, engines)
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch')
        if st.checkbox("Save to pack"):
            for r in data:
                persist_bench_result(pack_dir, r["engine"], r["size"], r["fps"], r["latency_ms"])
            st.success("Saved.")
