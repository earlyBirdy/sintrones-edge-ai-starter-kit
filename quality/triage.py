
from __future__ import annotations
from pathlib import Path
import json, os, glob, hashlib, random, time
from typing import List, Dict, Any
from core.db import connect, migrate

TRIAGE_STATE = Path("logs/triage_queue.json")

def _hash_path(p: str) -> str:
    return hashlib.sha1(p.encode("utf-8")).hexdigest()[:10]

def build_queue_from_anomalies() -> List[Dict[str, Any]]:
    """Scan logs/anomalies for image files and produce a triage queue list.
    Each item: {id, path, score, label?, notes?}
    """
    root = Path("logs/anomalies")
    root.mkdir(parents=True, exist_ok=True)
    items: List[Dict[str, Any]] = []
    exts = (".jpg", ".jpeg", ".png", ".bmp")
    for p in sorted(root.rglob("*")):
        if p.suffix.lower() in exts and p.is_file():
            items.append({
                "id": _hash_path(str(p)),
                "path": str(p),
                "score": round(0.6 + random.random()*0.35, 3)  # 0.60 - 0.95
            })
    # Merge with existing saved labels/notes if present
    if TRIAGE_STATE.exists():
        try:
            saved = {it["id"]: it for it in json.loads(TRIAGE_STATE.read_text())}
            for it in items:
                if it["id"] in saved:
                    it.update({k:v for k,v in saved[it["id"]].items() if k in ("label","notes")})
        except Exception:
            pass
    return items

def save_queue(queue: List[Dict[str, Any]]) -> None:
    TRIAGE_STATE.parent.mkdir(parents=True, exist_ok=True)
    with TRIAGE_STATE.open("w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)

def add_triage_item(unit_id, score, defect_label, assignee=None, sla_hours=24, note=""):
    con = connect(); migrate(con)
    meta = {
        "score": score,
        "label": defect_label,
        "assignee": assignee,
        "sla_h": sla_hours,
        "note": note,
    }
    con.execute(
        "INSERT INTO events(ts, device_id, severity, type, message, meta_json) "
        "VALUES (datetime('now'), 'local', 'info', 'triage_add', ?, json(?))",
        (f"unit:{unit_id}", json.dumps(meta))
    )
    con.commit()
