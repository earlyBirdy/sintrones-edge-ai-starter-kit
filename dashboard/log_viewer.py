import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

LOG_ROOT = Path("logs")

def _iter_files(root: Path, include_subdirs: bool):
    if not root.exists():
        return []
    if include_subdirs:
        return [p for p in root.rglob("*") if p.is_file()]
    return [p for p in root.iterdir() if p.is_file()]

def _human(n):
    if n < 1024: return f"{n} B"
    kb = n/1024
    if kb < 1024: return f"{kb:.1f} KB"
    mb = kb/1024
    return f"{mb:.1f} MB"

def _is_header_only_csv(p: Path) -> bool:
    try:
        with p.open("r", encoding="utf-8", errors="ignore") as f:
            head = [next(f, "").strip() for _ in range(3)]
        non_empty = [ln for ln in head[1:] if ln]
        return ("," in (head[0] or "")) and (len(non_empty) == 0)
    except Exception:
        return False

def _default_file_choice(paths):
    def score(p: Path):
        if p.suffix == ".log": return 0
        if p.suffix == ".jsonl": return 1
        if p.suffix == ".csv": return 2 if not _is_header_only_csv(p) else 5
        return 4
    if not paths: return None
    return sorted(paths, key=score)[0]

def render_log_viewer():
    st.title("📁 Log Viewer")
    st.caption("Browse files under `./logs` with a lookback filter.")

    if not LOG_ROOT.exists():
        st.warning("`logs/` folder not found. Create it or run the bootstrap to generate samples.")
        return

    with st.expander("Filters"):
        hours = st.slider("Lookback hours", 1, 168, 24, 1)
        exts = st.multiselect("Extensions", [".log",".jsonl",".csv",".txt"], [".log",".jsonl",".csv",".txt"])
        q = st.text_input("Filename contains", "")
        show_subdirs = st.checkbox("Include subdirectories", True)
        preview_rows = st.slider("Preview last N lines (jsonl/txt/log)", 0, 500, 50, 10)

    cutoff = datetime.now() - timedelta(hours=hours)
    paths = []
    for p in _iter_files(LOG_ROOT, show_subdirs):
        if exts and p.suffix not in exts: continue
        if q and q.lower() not in p.name.lower(): continue
        try:
            stat = p.stat()
        except Exception:
            continue
        mtime = datetime.fromtimestamp(stat.st_mtime)
        if mtime < cutoff: continue
        paths.append(p)

    if not paths:
        st.info("No files match your filters (try increasing lookback or enabling subdirectories).")
        return

    rows = [{
        "name": p.name,
        "size": _human(p.stat().st_size),
        "modified": datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds"),
        "path": p.as_posix()
    } for p in paths]

    df = pd.DataFrame(rows)
    if "modified" in df.columns:
        df = df.sort_values("modified", ascending=False)
    st.dataframe(df, width='stretch', height=360)

    default_path = _default_file_choice(paths)
    choices = df["path"].tolist()
    idx = choices.index(default_path.as_posix()) if default_path else 0
    sel = st.selectbox("Select a file to preview / download", choices, index=idx)

    if sel:
        p = Path(sel)
        st.download_button(f"Download {p.name}", data=p.read_bytes(), file_name=p.name)

        if p.suffix == ".csv":
            try:
                dfc = pd.read_csv(p)
                if dfc.empty:
                    st.caption("CSV has headers but no rows yet.")
                else:
                    st.dataframe(dfc, width='stretch', height=420)
            except Exception as e:
                st.error(f"CSV preview failed: {e}")
            return

        if preview_rows > 0 and p.suffix in {".jsonl",".log",".txt"}:
            try:
                with p.open("rb") as f:
                    f.seek(0,2)
                    end = f.tell()
                    chunk = 4096
                    data = b""
                    count = 0
                    pos = end
                    while pos > 0 and count < preview_rows:
                        read = min(chunk, pos)
                        pos -= read
                        f.seek(pos)
                        data = f.read(read) + data
                        count = data.count(b"\n")
                    lines = data.splitlines()[-preview_rows:]
                st.text("\n".join([ln.decode(errors="replace") for ln in lines]))
            except Exception as e:
                st.error(f"Preview failed: {e}")
