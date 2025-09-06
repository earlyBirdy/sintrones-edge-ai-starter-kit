import streamlit as st
import pandas as pd
import os
import json

def show_benchmark_viewer():
    st.subheader("📈 Model Performance Benchmark")
    benchmark_file = "benchmarks/benchmark.json"
    if os.path.exists(benchmark_file):
        with open(benchmark_file, "r") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        if "runtime" in df.columns:
            st.bar_chart(df.set_index("runtime")[["fps", "latency_ms"]])
        else:
            st.warning("Benchmark file missing 'runtime' column.")
    else:
        st.info("No benchmark file found at benchmarks/benchmark.json")