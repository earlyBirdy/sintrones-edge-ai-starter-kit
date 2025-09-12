import os, json, glob, hashlib
import pandas as pd
from datetime import datetime
def _safe_load_json(p):
    try:
        with open(p,"r",encoding="utf-8") as f: return json.load(f)
    except Exception: return {}
def _hash_file(p):
    if not os.path.exists(p): return ""
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(65536), b""): h.update(c)
    return h.hexdigest()
def build_trace_index(log_root="logs") -> pd.DataFrame:
    rows=[]
    ev=os.path.join(log_root,"events.jsonl")
    if os.path.exists(ev):
        with open(ev,"r",encoding="utf-8") as f:
            for line in f:
                if not line.strip(): continue
                try: evt=json.loads(line)
                except Exception: continue
                evt["source"]="events.jsonl"; rows.append(evt)
    for rel in ["anomalies","pass","fail","samples"]:
        d=os.path.join(log_root, rel)
        if not os.path.isdir(d): continue
        for p in glob.glob(os.path.join(d,"*")):
            if os.path.isdir(p): continue
            if p.lower().endswith((".jpg",".jpeg",".png",".bmp",".tif",".tiff")):
                side=os.path.splitext(p)[0]+".json"; meta=_safe_load_json(side) if os.path.exists(side) else {}
                rows.append({"ts":meta.get("timestamp"),"unit_id":meta.get("unit_id"),"station_id":meta.get("station_id"),
                             "camera_id":meta.get("camera_id"),"model":meta.get("model"),"model_version":meta.get("model_version"),
                             "result":meta.get("result","PREDICT"),"score":meta.get("score"),"label":meta.get("label"),
                             "artifact_path":p.replace('\\','/'),"artifact_sha256":_hash_file(p),"source":rel})
    if not rows:
        return pd.DataFrame(columns=["ts","unit_id","station_id","shift","camera_id","model","model_version","result","score","label","artifact_path","artifact_sha256","source"])
    df=pd.DataFrame(rows)
    def _parse_ts(x):
        if x is None: return None
        try: return datetime.fromisoformat(x.replace("Z","+00:00"))
        except Exception: return None
    df["parsed_ts"]=df["ts"].apply(_parse_ts) if "ts" in df.columns else None
    df["day"]=df["parsed_ts"].dt.date if "parsed_ts" in df.columns and df["parsed_ts"].notna().any() else None
    df["has_label"]=df.get("label").notna() if "label" in df.columns else False
    return df
