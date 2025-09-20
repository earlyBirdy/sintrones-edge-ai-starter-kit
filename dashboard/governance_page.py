
import streamlit as st
from pathlib import Path

def render_governance():
    st.subheader("🔐 Governance")
    st.markdown("""
This page outlines lightweight governance helpers for datasets, models, and deployments.
Use these commands in your repo root. The widgets are placeholders you can wire to your real tooling.
""")

    st.markdown("**Dataset tracking (DVC)**")
    st.code("dvc status\n"
            "dvc add data/raw\n"
            "dvc push", language="bash")

    st.markdown("**Model registry (MLflow-like)**")
    st.code("mlflow run .\n"
            "mlflow models serve -m runs:/<run_id>/model", language="bash")

    st.markdown("**Reproducible environment (conda + lock)**")
    st.code("conda env create -f environment.yml\n"
            "conda activate sintrones-edge-ai\n"
            "pip install -r requirements.txt", language="bash")

    st.markdown("**Security & compliance checklist**")
    st.checkbox("All 3rd‑party licenses audited", value=False, key="lic")
    st.checkbox("PII handling validated / no PII stored", value=False, key="pii")
    st.checkbox("Model cards updated with version and eval metrics", value=False, key="cards")
    st.checkbox("SBOM generated for release artifacts", value=False, key="sbom")

    st.info("Tip: Replace these placeholders with your internal scripts and status checks.")
