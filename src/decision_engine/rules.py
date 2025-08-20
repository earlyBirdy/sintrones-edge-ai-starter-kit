from typing import Dict, Tuple

LEVELS = ["NONE", "WARN", "ALERT", "SHUTDOWN"]

def _compare_level(a: str, b: str) -> str:
    return a if LEVELS.index(a) >= LEVELS.index(b) else b

def evaluate_rule(event: Dict, thresholds: Dict) -> Tuple[str, Dict]:
    level = "NONE"; reasons = {}
    t = event.get("temperature")
    if isinstance(t, (int, float)) and "temperature" in thresholds:
        th = thresholds["temperature"]; w = th.get("warn"); a = th.get("alert")
        if a is not None and t >= a:
            level = _compare_level(level, "ALERT"); reasons.setdefault("temperature", []).append(("ALERT", t, a))
        elif w is not None and t >= w:
            level = _compare_level(level, "WARN"); reasons.setdefault("temperature", []).append(("WARN", t, w))
    v = event.get("vibration")
    if isinstance(v, (int, float)) and "vibration" in thresholds:
        th = thresholds["vibration"]; w = th.get("warn"); a = th.get("alert")
        if a is not None and v >= a:
            level = _compare_level(level, "ALERT"); reasons.setdefault("vibration", []).append(("ALERT", v, a))
        elif w is not None and v >= w:
            level = _compare_level(level, "WARN"); reasons.setdefault("vibration", []).append(("WARN", v, w))
    dets = event.get("detections") or []
    if isinstance(dets, list) and "defects_per_frame" in thresholds:
        th = thresholds["defects_per_frame"]
        warn = th.get("warn"); alert = th.get("alert")
        n = len(dets)
        if alert is not None and n >= alert:
            level = _compare_level(level, "ALERT"); reasons.setdefault("defects_per_frame", []).append(("ALERT", n, alert))
        elif warn is not None and n >= warn:
            level = _compare_level(level, "WARN"); reasons.setdefault("defects_per_frame", []).append(("WARN", n, warn))
    if event.get("anomaly") is True:
        level = _compare_level(level, "ALERT")
    return level, reasons
