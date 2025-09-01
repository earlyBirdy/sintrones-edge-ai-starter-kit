
# Streamlit UI for On-Device Fine Tuning (Template)
import streamlit as st

st.title("Edge AI Few-Shot Fine-Tuning")
st.info("Label a few anomaly frames, generate ONNX update template.")

uploaded = st.file_uploader("Upload anomaly image", type=["jpg", "png"])
if uploaded:
    st.image(uploaded)
    label = st.selectbox("Label this image as:", ["OK", "NG-Defect1", "NG-Defect2"])
    st.success(f"Labeled as: {label} (save to template for ONNX)")
