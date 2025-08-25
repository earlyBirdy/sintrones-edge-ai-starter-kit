import streamlit as st
import os
import json
import cv2
from PIL import Image

LOG_DIR = "logs"

st.set_page_config(page_title="Vision Inspection Logs", layout="wide")
st.title("📸 Vision Inspection Log Viewer")

if not os.path.exists(LOG_DIR):
    st.warning(f"No logs found in {LOG_DIR}/")
    st.stop()

# Load logs
images = sorted([f for f in os.listdir(LOG_DIR) if f.endswith(".jpg")])
if not images:
    st.info("No image logs found.")
    st.stop()

selected_img = st.selectbox("Select Logged Frame", images)
img_path = os.path.join(LOG_DIR, selected_img)
meta_path = img_path.replace(".jpg", ".json")

col1, col2 = st.columns([2, 1])

# Show image
with col1:
    st.image(img_path, caption=selected_img, use_column_width=True)

# Show metadata
with col2:
    st.subheader("📄 Metadata")
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            metadata = json.load(f)
        st.json(metadata)
    else:
        st.error("Metadata file not found.")

# Optional filters (e.g., pass/fail)
statuses = [json.load(open(os.path.join(LOG_DIR, f.replace('.jpg', '.json')))).get("status", "UNKNOWN") for f in images if os.path.exists(os.path.join(LOG_DIR, f.replace('.jpg', '.json')))]
if statuses:
    st.sidebar.write("🧮 Status Summary")
    for status in set(statuses):
        st.sidebar.write(f"- {status}: {statuses.count(status)}")