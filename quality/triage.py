import os, json, time

def build_queue_from_anomalies(log_dir="logs/anomalies"):
    items=[]
    if os.path.isdir(log_dir):
        for fn in sorted(os.listdir(log_dir))[:50]:
            if fn.lower().endswith((".jpg",".png",".jpeg")):
                items.append({"id":fn, "path":os.path.join(log_dir,fn), "score":0.9, "ts":time.time(), "label":None})
    return items

def save_queue(queue, path="logs/triage_queue.jsonl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w") as f:
        for r in queue: f.write(json.dumps(r)+"\n")

def promote_to_rule(record, roi=None, threshold=0.85, rule_dir="recipes/rules"):
    os.makedirs(rule_dir, exist_ok=True)
    rule_path = os.path.join(rule_dir, f"rule_{record['id']}.yaml")
    with open(rule_path,"w") as f:
        f.write(f"id: rule_{record['id']}\n")
        f.write("type: roi_threshold\n")
        f.write(f"value: {threshold}\n")
        if roi: f.write(f"roi: {roi}\n")
    return rule_path
