
import os
import json
from datetime import datetime
from typing import List, Dict, Optional
import pandas as pd

def _parse_ts_from_name(name: str) -> Optional[datetime]:
    import re, time
    m = re.search(r"(\d{10})", name)  # epoch seconds
    if m:
        try:
            return datetime.fromtimestamp(int(m.group(1)))
        except Exception:
            pass
    for fmt in ["%Y-%m-%d_%H-%M-%S", "%Y%m%d_%H%M%S", "%Y-%m-%d-%H-%M-%S"]:
        try:
            return datetime.strptime(os.path.splitext(name)[0], fmt)
        except Exception:
            continue
    return None

def _read_json_sidecar(path_no_ext: str) -> Dict:
    meta_path = f"{path_no_ext}.json"
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def build_trace_index(log_root: str = "logs") -> pd.DataFrame:
    rows: List[Dict] = []
    anomalies_dir = os.path.join(log_root, "anomalies")
    if os.path.isdir(anomalies_dir):
        for fn in os.listdir(anomalies_dir):
            if fn.lower().endswith((".jpg",".jpeg",".png")):
                fpath = os.path.join(anomalies_dir, fn)
                path_no_ext = os.path.splitext(fpath)[0]
                stat = os.stat(fpath)
                meta = _read_json_sidecar(path_no_ext)
                ts = meta.get("timestamp") or _parse_ts_from_name(fn)
                if isinstance(ts, str):
                    try:
                        ts = datetime.fromisoformat(ts)
                    except Exception:
                        ts = None
                rows.append({
                    "path": fpath,
                    "filename": fn,
                    "kind": "anomaly_image",
                    "ts": ts,
                    "size_bytes": stat.st_size,
                    "label": meta.get("label"),
                    "result": meta.get("result") or meta.get("status"),
                    "model_version": meta.get("model_version"),
                    "device_id": meta.get("device_id"),
                    "extra": {k:v for k,v in meta.items() if k not in {"timestamp","label","result","status","model_version","device_id"}}
                })
    if os.path.isdir(log_root):
        for fn in os.listdir(log_root):
            if fn.lower().endswith(".jsonl"):
                fpath = os.path.join(log_root, fn)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue
                            try:
                                obj = json.loads(line)
                            except Exception:
                                obj = {}
                            ts = obj.get("timestamp") or obj.get("ts")
                            if isinstance(ts, (int,float)):
                                ts = datetime.fromtimestamp(ts)
                            elif isinstance(ts, str):
                                try:
                                    ts = datetime.fromisoformat(ts)
                                except Exception:
                                    ts = None
                            rows.append({
                                "path": fpath,
                                "filename": fn,
                                "kind": "jsonl_event",
                                "ts": ts,
                                "size_bytes": None,
                                "label": obj.get("label"),
                                "result": obj.get("result") or obj.get("status"),
                                "model_version": obj.get("model_version"),
                                "device_id": obj.get("device_id"),
                                "extra": obj
                            })
                except Exception:
                    pass
    df = pd.DataFrame(rows)
    if not df.empty and "ts" in df.columns:
        df = df.sort_values(by="ts", ascending=False, na_position="last").reset_index(drop=True)
    return df

def summarize_trace_index(df: pd.DataFrame) -> Dict:
    if df is None or df.empty:
        return {
            "total_records": 0,
            "anomaly_images": 0,
            "json_events": 0,
            "labels": {},
            "results": {}
        }
    labels = df["label"].dropna().astype(str).value_counts().to_dict() if "label" in df else {}
    results = df["result"].dropna().astype(str).value_counts().to_dict() if "result" in df else {}
    return {
        "total_records": int(len(df)),
        "anomaly_images": int((df["kind"]=="anomaly_image").sum()) if "kind" in df else 0,
        "json_events": int((df["kind"]=="jsonl_event").sum()) if "kind" in df else 0,
        "labels": labels,
        "results": results
    }
