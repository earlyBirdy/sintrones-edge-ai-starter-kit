import os, glob, yaml, time
RULE_DIR="recipes/rules"
def list_rules(rule_dir=RULE_DIR):
    os.makedirs(rule_dir, exist_ok=True); rows=[]
    for p in glob.glob(os.path.join(rule_dir,"*.yaml")):
        try:
            y=yaml.safe_load(open(p))
        except Exception:
            y={}
        rows.append({"rule_file":p,"id":y.get("id"),"type":y.get("type"),"value":y.get("value")})
    return rows
def promote_to_rule(record, roi=None, threshold=0.85, rule_dir=RULE_DIR):
    os.makedirs(rule_dir, exist_ok=True)
    p=os.path.join(rule_dir, f"rule_{int(time.time())}_{record['id'].split('.')[0]}.yaml")
    y={"id":f"rule_{record['id']}", "type":"roi_threshold" if roi else "threshold","value":float(threshold),"roi":roi,"source_image":record.get("path"),"created_at":time.strftime("%Y-%m-%dT%H:%M:%S")}
    yaml.safe_dump(y, open(p,"w")); return p
