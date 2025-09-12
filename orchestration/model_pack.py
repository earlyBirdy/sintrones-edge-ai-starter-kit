import os, json, yaml, time, hashlib
REQUIRED_KEYS = ["model_id", "version", "artifacts"]
def load_model_pack(path): 
    y=os.path.join(path,"modelpack.yaml")
    if not os.path.exists(y): return {}
    with open(y,"r",encoding="utf-8") as f: 
        return yaml.safe_load(f) or {}
def save_model_pack(path, pack): 
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path,"modelpack.yaml"),"w",encoding="utf-8") as f: 
        yaml.safe_dump(pack, f, sort_keys=False)
def validate_pack(pack):
    issues=[]; 
    if not pack: return [{"level":"error","message":"modelpack.yaml missing"}]
    for k in REQUIRED_KEYS: 
        if k not in pack: issues.append({"level":"error","message":f"Missing key: {k}"})
    if "onnx" not in pack.get("artifacts",{}) and "tensorrt" not in pack.get("artifacts",{}):
        issues.append({"level":"warn","message":"No ONNX/TensorRT artifact"})
    return issues
def _sha256(p):
    if not os.path.exists(p): return ""
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for c in iter(lambda:f.read(65536), b""): h.update(c)
    return h.hexdigest()
def smoke_test(pack_dir):
    pack=load_model_pack(pack_dir); arts=pack.get("artifacts",{})
    res={"artifacts":{}, "tests":{}}
    for k,v in (arts or {}).items():
        p=os.path.join(pack_dir,v)
        res["artifacts"][k]={"exists":os.path.exists(p),"sha256":_sha256(p) if os.path.exists(p) else ""}
    img=os.path.join(pack_dir,"tests","smoke.jpg")
    res["tests"]["smoke.jpg"]={"exists":os.path.exists(img)}
    res["status"]="ok" if all(a["exists"] for a in res["artifacts"].values()) else "warn"
    return res
def select_engine(pack, hw_caps): 
    pref=(pack or {}).get("runtime",{}).get("preferred")
    if pref: return pref
    accel=(hw_caps or {}).get("accel","cpu").lower()
    if accel in ("gpu","cuda","jetson"): return "tensorrt"
    if accel in ("intel","xpu","igpu"): return "openvino"
    return "onnxruntime"
def persist_bench_result(pack_dir, engine, size, fps, latency_ms):
    pack=load_model_pack(pack_dir); pack.setdefault("benchmarks",{})
    today=time.strftime("%Y-%m-%d"); pack["benchmarks"].setdefault(today,{})
    pack["benchmarks"][today][engine]={"fps":float(fps),"latency_ms":float(latency_ms),"size":str(size)}
    save_model_pack(pack_dir, pack)
def deploy_pack(pack_dir, device_id):
    pack=load_model_pack(pack_dir); os.makedirs("deployments", exist_ok=True)
    with open(os.path.join("deployments",f"{device_id}.json"),"w",encoding="utf-8") as f:
        json.dump({"device_id":device_id,"model_id":pack.get("model_id"),"version":pack.get("version"),
                   "pack_dir":os.path.abspath(pack_dir),"deployed_at":time.strftime("%Y-%m-%dT%H:%M:%S")}, f, indent=2)
    return {"status":"ok","device_id":device_id}
def rollback(device_id):
    p=os.path.join("deployments",f"{device_id}.json")
    if os.path.exists(p): os.remove(p); return {"status":"rolled_back","device_id":device_id}
    return {"status":"noop","device_id":device_id}
