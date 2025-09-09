import time
import streamlit as st

def run():
    st.title("📂 Sample Example Script")
    st.write("This is a basic example script to demonstrate functionality.")
    for i in range(5):
        st.write(f"Processing step {i + 1}...")
        time.sleep(0.5)
    st.success("Done!")