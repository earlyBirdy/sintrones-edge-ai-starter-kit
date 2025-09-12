import os, json, time
def _score_from_name(name): return 0.9 if any(k in name.lower() for k in ["ng","defect"]) else 0.6
def build_queue_from_anomalies(log_dir="logs/anomalies"):
    items=[]
    if os.path.isdir(log_dir):
        for fn in sorted(os.listdir(log_dir))[-200:]:
            if fn.lower().endswith((".jpg",".png",".jpeg")):
                items.append({"id":fn,"path":os.path.join(log_dir,fn),"score":_score_from_name(fn),"ts":time.time(),"label":None,"notes":""})
    items.sort(key=lambda r:(-r["score"], -r["ts"])); return items
def save_queue(queue, path="logs/triage_queue.jsonl"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w") as f:
        for r in queue: f.write(json.dumps(r)+"\n")
