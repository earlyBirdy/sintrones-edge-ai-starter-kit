import streamlit as st
import pandas as pd
from bench.benchmark_matrix import run_matrix

def render_benchmark_matrix():
    st.subheader("📊 Benchmark Matrix")
    df = pd.DataFrame(run_matrix())
    st.dataframe(df, use_container_width=True)
