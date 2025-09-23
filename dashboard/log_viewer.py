# dashboard/log_viewer.py
# Minimal file-based Log Viewer: ONLY scans ./logs for files, lists them, and previews the selected file.
import os
from pathlib import Path
import streamlit as st
import pandas as pd
import json

LOGS_DIR = Path.cwd() / "logs"
PATTERNS = ["*.csv", "*.log", "*.jsonl"]  # restrict types under /logs

def _discover_logs():
    if not LOGS_DIR.exists():
        return []
    files = []
    for pat in PATTERNS:
        files += sorted(LOGS_DIR.rglob(pat), key=lambda p: p.as_posix())
    return files

def _load_any(path: Path) -> pd.DataFrame:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix == ".jsonl":
        rows = []
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    rows.append({"raw": line})
        return pd.DataFrame(rows)
    # .log or others -> try CSV first, else raw text as single column
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame({"line": path.read_text(encoding="utf-8", errors="ignore").splitlines()})

def render_log_viewer():
    st.subheader("✅ Anomaly Log Viewer")
    st.caption("Showing files from ./logs")

    logs = _discover_logs()
    if not logs:
        st.info("No log files found under ./logs. Put .csv / .log / .jsonl files there.")
        return

    # Prefer a file named like '*anomaly*.csv' if available
    default_idx = 0
    for i, p in enumerate(logs):
        if "anomaly" in p.name.lower() and p.suffix.lower() == ".csv":
            default_idx = i
            break

    choice = st.selectbox("Select a log file", [str(p.relative_to(Path.cwd())) for p in logs], index=default_idx)
    path = Path.cwd() / choice

    try:
        df = _load_any(path)
    except Exception as e:
        st.error(f"Failed to load {choice}: {e}")
        return

    # Friendly timestamp parsing if present
    for col in ("timestamp", "ts", "time"):
        if col in df.columns:
            try:
                df[col] = pd.to_datetime(df[col]).astype(str)
            except Exception:
                pass

    st.dataframe(df, use_container_width=True, height=480)
    st.download_button("Download selected file", data=path.read_bytes(), file_name=path.name)

# Back-compat entry point if app.py still uses old name
def show_log_viewer():
    render_log_viewer()
