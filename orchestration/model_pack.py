import os, yaml, json
from dataclasses import dataclass

@dataclass
class PackValidationIssue:
    level: str
    message: str

def load_model_pack(path:str)->dict:
    y = os.path.join(path, "modelpack.yaml")
    if not os.path.exists(y): return {}
    with open(y, "r") as f: return yaml.safe_load(f)

def validate_pack(pack:dict)->list[PackValidationIssue]:
    issues=[]
    if not pack: issues.append(PackValidationIssue("error","Missing modelpack.yaml"))
    if pack and "artifacts" not in pack: issues.append(PackValidationIssue("error","artifacts section missing"))
    return issues

def select_engine(pack:dict, hw_caps:dict)->str:
    return (pack or {}).get("runtime",{}).get("preferred","onnxruntime")

def deploy_pack(pack:dict, device_id:str)->dict:
    os.makedirs("deployments", exist_ok=True)
    with open(os.path.join("deployments", f"{device_id}.json"),"w") as f:
        json.dump({"device_id":device_id,"active_pack":(pack or {}).get("version","N/A")}, f)
    return {"status":"ok"}

def rollback(device_id:str)->dict:
    p = os.path.join("deployments", f"{device_id}.json")
    return {"status":"ok" if os.path.exists(p) else "noop"}
