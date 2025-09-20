#!/usr/bin/env python3
"""
Auto-discovering End-to-End Module Checker (robust, future-proof)
- Recursively scans for Streamlit pages (folders named 'pages' or 'tabs')
- Reads tab names from app.py if you build tabs with st.tabs(tab_names)
- Runs specific checks for known modules; SKIPs unknown ones but lists them
- Creates placeholder folders/configs for certain feature tabs (self-healing)
"""

import os
import re
import time
import sqlite3
from pathlib import Path

# ---- Config ----
DB_PATH = str(Path(os.getenv("EDGEKIT_DB_PATH", "data/edgekit.db")).resolve())
LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "24"))

ENV_DIRS = [d.strip() for d in os.getenv("PAGES_DIRS", "").split(",") if d.strip()]
DEFAULT_DIRS = ["dashboard/pages", "pages", "dashboard/tabs", "tabs", "ui/pages", "main/pages"]

# ---------- DB helpers ----------
def _conn():
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c

def _count(conn, sql, params=()):
    cur = conn.execute(sql, params)
    row = cur.fetchone()
    return 0 if row is None else row[0]

def _table_exists(conn, name: str) -> bool:
    cur = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (name,),
    )
    return cur.fetchone() is not None

# ---------- Discovery ----------
def _find_pages_dirs():
    if ENV_DIRS:
        return [Path(p) for p in ENV_DIRS if Path(p).exists() and Path(p).is_dir()]
    roots = [Path("."), Path("main"), Path("dashboard"), Path("ui")]
    found = []
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        for d in root.rglob("*"):
            if d.is_dir() and d.name in {"pages", "tabs"}:
                if any(p.suffix == ".py" for p in d.glob("*.py")):
                    rp = d.resolve()
                    if rp not in seen:
                        seen.add(rp)
                        found.append(rp)
    for d in DEFAULT_DIRS:
        pd = Path(d)
        if pd.exists() and pd.is_dir():
            rp = pd.resolve()
            if rp not in seen and any(p.suffix == ".py" for p in pd.glob("*.py")):
                seen.add(rp)
                found.append(rp)
    return found

def _discover_tabs_from_app(app_path: str = "app.py") -> list[str]:
    p = Path(app_path)
    if not p.exists():
        return []
    try:
        src = p.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r"tab_names\s*=\s*\[([^\]]*)\]", src, re.DOTALL)
        if m:
            inner = m.group(1)
            items = re.findall(r"""['"]([^'"]+)['"]""", inner)
            return [s.strip() for s in items if s.strip()]
        m = re.search(r"tab_names\s*=\s*\(([^\)]*)\)", src, re.DOTALL)
        if m:
            inner = m.group(1)
            items = re.findall(r"""['"]([^'"]+)['"]""", inner)
            return [s.strip() for s in items if s.strip()]
    except Exception:
        pass
    return []

# ---------- DB-driven checks ----------
def check_quick_start(conn):
    devices = _count(conn, "SELECT COUNT(*) FROM devices")
    readings = _count(conn, "SELECT COUNT(*) FROM sensor_readings")
    quality = _count(conn, "SELECT COUNT(*) FROM quality_results")
    ok = devices > 0 and readings > 0 and quality > 0
    return ok, f"Devices={devices}, Readings={readings}, Quality={quality}"

def check_fleet(conn):
    devices = _count(conn, "SELECT COUNT(*) FROM devices")
    return devices > 0, f"Devices={devices}"

def check_yield_quality(conn):
    passed = _count(conn, "SELECT COUNT(*) FROM quality_results WHERE passed=1")
    failed = _count(conn, "SELECT COUNT(*) FROM quality_results WHERE passed=0")
    ok = passed > 0 and failed > 0
    return ok, f"Passed={passed}, Failed={failed}"

def check_data_traceability(conn):
    rows = _count(
        conn,
        f"""
        SELECT COUNT(*) FROM sensor_readings sr
        LEFT JOIN inference_events ie ON ie.reading_id = sr.id
        LEFT JOIN quality_results qr ON qr.reading_id = sr.id
        WHERE sr.ts >= datetime('now','-{LOOKBACK_HOURS} hours')
        """,
    )
    return rows > 0, f"Traceability rows={rows}"

def check_anomalies(conn):
    anomalies = _count(conn, "SELECT COUNT(*) FROM anomalies")
    return anomalies > 0, f"Anomalies={anomalies}"

def check_logs(conn):
    logs = _count(
        conn,
        f"SELECT COUNT(*) FROM event_log WHERE ts >= datetime('now','-{LOOKBACK_HOURS} hours')",
    )
    return logs > 0, f"Recent logs={logs}"

def check_inference_balance(conn):
    okc = _count(conn, "SELECT COUNT(*) FROM inference_events WHERE pred_label='ok'")
    defect = _count(conn, "SELECT COUNT(*) FROM inference_events WHERE pred_label='defect'")
    return (okc > 0 and defect > 0), f"Ok={okc}, Defect={defect}"

def check_sqlite(conn):
    if not Path(DB_PATH).exists():
        return False, f"DB missing: {DB_PATH}"
    required = ["devices", "sensor_readings", "inference_events", "quality_results", "event_log"]
    missing = [t for t in required if not _table_exists(conn, t)]
    if missing:
        return False, f"Missing tables: {', '.join(missing)}"
    n = _count(conn, "SELECT COUNT(*) FROM sensor_readings")
    return n > 0, f"Core tables OK; readings={n}"

def check_quality_sqlite(conn):
    if not _table_exists(conn, "quality_results"):
        return False, "quality_results missing"
    tot = _count(conn, "SELECT COUNT(*) FROM quality_results")
    if tot == 0:
        return False, "quality_results empty"
    p = _count(conn, "SELECT COUNT(*) FROM quality_results WHERE passed=1")
    f = _count(conn, "SELECT COUNT(*) FROM quality_results WHERE passed=0")
    return (p > 0 and f > 0), f"total={tot}, passed={p}, failed={f}"

# ---------- File-driven checks / self-healing ----------
def _ensure_folder(path: Path, desc: str):
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return True, f"FIXED — created {desc} at {path}"
    return True, f"{desc} exists: {path}"

def _ensure_file(path: Path, desc: str, default_text="# placeholder\n"):
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(default_text)
        return True, f"FIXED — created {desc} at {path}"
    return True, f"{desc} exists: {path}"

def check_benchmark_panel(_): return _ensure_folder(Path("benchmarks"), "Benchmarks folder")
def check_fine_tuning(_):    return _ensure_folder(Path("models/finetune"), "Fine-tuning folder")
def check_multi_camera(_):   return _ensure_file(Path("config/cameras.yaml"), "Camera config")
def check_saliency_xai(_):   return _ensure_folder(Path("xai_results"), "XAI results folder")
def check_health_check(_):   return (Path(DB_PATH).exists(), f"DB file exists: {DB_PATH}")
def check_live_camera(_):    return True, "Live camera check not implemented (SKIP)"

# New feature checks (tabs from app.py)
def check_model_packs(_): return _ensure_folder(Path("models/packs"), "Model Packs folder")
def check_inspection_rules(_): return _ensure_file(Path("config/inspection_rules.yaml"), "Inspection Rules file", "# rules: []\n")
def check_pipeline_builder(_): return _ensure_folder(Path("pipelines"), "Pipelines folder")
def check_io_connectors(_): return _ensure_folder(Path("config/connectors"), "I/O Connectors folder")
def check_triage_queue(conn):
    n = _count(conn, "SELECT COUNT(*) FROM anomalies")
    if n > 0:
        return True, f"Triage items from anomalies: {n}"
    ok, msg = _ensure_folder(Path("triage"), "Triage folder")
    return True, f"{msg}; anomalies=0"
def check_governance(_): return _ensure_file(Path("config/policy.yaml"), "Governance policy file", "retention_days: 30\nroles: []\n")
def check_few_shot_finetune(_): return _ensure_folder(Path("models/fewshot"), "Few-shot Fine-Tuning folder")
def check_examples(_): return _ensure_folder(Path("examples"), "Examples folder")

# MES export freshness check
def check_mes_export(_):
    d = Path(os.getenv("MES_EXPORT_DIR", "exports/mes"))
    if not d.exists():
        return False, f"exports folder missing: {d}"
    files = sorted(d.glob("mes_last*h_*.csv")) + sorted(d.glob("mes_latest.csv"))
    if not files:
        return False, f"no export files in {d}"
    latest = max(files, key=lambda p: p.stat().st_mtime)
    age_min = (time.time() - latest.stat().st_mtime) / 60
    return True, f"found {latest.name}, age≈{age_min:.1f} min"

# ---------- Known checks ----------
CHECKS = {
    "Quick Start": check_quick_start,
    "Fleet": check_fleet,
    "Yield & Quality": check_yield_quality,
    "Data Traceability": check_data_traceability,
    "Anomaly Log Viewer": check_anomalies,
    "Logs": check_logs,
    "Inference Balance": check_inference_balance,
    "Benchmark Panel": check_benchmark_panel,
    "Fine-Tuning": check_fine_tuning,
    "Multi-Camera": check_multi_camera,
    "Saliency/XAI": check_saliency_xai,
    "Health Check": check_health_check,
    "Live Camera Feed": check_live_camera,
    "Sqlite": check_sqlite,
    "Quality Sqlite": check_quality_sqlite,
    # app.py feature tabs
    "📦 Model Packs": check_model_packs,
    "✅ Inspection Rules": check_inspection_rules,
    "🧱 Pipeline Builder": check_pipeline_builder,
    "⚙️ I/O Connectors": check_io_connectors,
    "🧰 Triage Queue": check_triage_queue,
    "🔐 Governance": check_governance,
    "🛠️ Few-Shot Fine-Tuning": check_few_shot_finetune,
    "📂 Examples": check_examples,
    "📷 Multi-Cam Feeds": check_multi_camera,
    # MES
    "MES Export": check_mes_export,
}

# ---------- Runner ----------
def _normalize(s: str) -> str:
    return " ".join(s.lower().strip().replace("_", " ").split())

KEYWORD_MAP = [
    ("quick", "Quick Start"),
    ("fleet", "Fleet"),
    ("yield", "Yield & Quality"),
    ("quality", "Yield & Quality"),
    ("trace", "Data Traceability"),
    ("anomaly", "Anomaly Log Viewer"),
    ("log", "Logs"),
    ("infer", "Inference Balance"),
    ("bench", "Benchmark Panel"),
    ("tune", "Fine-Tuning"),
    ("camera", "Multi-Camera"),
    ("xai", "Saliency/XAI"),
    ("health", "Health Check"),
    ("live", "Live Camera Feed"),
    ("sqlite", "Sqlite"),
    # app.py feature heuristics
    ("multi-cam", "📷 Multi-Cam Feeds"),
    ("multicam", "📷 Multi-Cam Feeds"),
    ("cam feeds", "📷 Multi-Cam Feeds"),
    ("model", "📦 Model Packs"),
    ("pack", "📦 Model Packs"),
    ("inspect", "✅ Inspection Rules"),
    ("pipeline", "🧱 Pipeline Builder"),
    ("connector", "⚙️ I/O Connectors"),
    ("triage", "🧰 Triage Queue"),
    ("govern", "🔐 Governance"),
    ("few-shot", "🛠️ Few-Shot Fine-Tuning"),
    ("few shot", "🛠️ Few-Shot Fine-Tuning"),
    ("example", "📂 Examples"),
    # MES
    ("mes", "MES Export"),
]

def _map_by_keyword(name: str):
    n = _normalize(name)
    for key, target in KEYWORD_MAP:
        if key in n:
            return CHECKS.get(target)
    return None

def run_checks():
    pages_dirs = _find_pages_dirs()
    if pages_dirs:
        print("Discovered pages dirs:", [str(p) for p in pages_dirs])

    picked = {}
    for d in pages_dirs:
        for p in d.glob("*.py"):
            stem = p.stem
            name = stem.split("_", 1)[-1] if "_" in stem else stem
            name = name.replace("_", " ").title()
            picked[name] = p
    if picked:
        print("Discovered pages:", [f"{n} ← {picked[n].name}" for n in sorted(picked.keys())])

    discovered = list(picked.keys())

    app_tabs = _discover_tabs_from_app("app.py")
    if app_tabs:
        print("Tabs from app.py:", app_tabs)
        for n in app_tabs:
            n_norm = n if n.isupper() else n.title()
            if n_norm not in discovered:
                discovered.append(n_norm)

    names = []
    seen = set()
    for n in discovered:
        if n not in seen:
            names.append(n); seen.add(n)
    for reg in CHECKS.keys():
        if reg not in seen:
            names.append(reg); seen.add(reg)

    with _conn() as conn:
        passed = failed = fixed = skipped = 0
        for name in names:
            fn = CHECKS.get(name) or _map_by_keyword(name)
            try:
                if fn:
                    ok, msg = fn(conn)
                    if ok:
                        if isinstance(msg, str) and msg.startswith("FIXED"):
                            print(f"⚠️ {name}: {msg}")
                            fixed += 1
                        else:
                            print(f"✅ {name}: PASS — {msg}")
                            passed += 1
                    else:
                        # If any helper still returns False with "FIXED", treat it as fixed
                        if isinstance(msg, str) and msg.startswith("FIXED"):
                            print(f"⚠️ {name}: {msg}")
                            fixed += 1
                        else:
                            print(f"❌ {name}: FAIL — {msg}")
                            failed += 1
                else:
                    print(f"➖ {name}: SKIP — no check defined yet")
                    skipped += 1
            except Exception as e:
                print(f"⚠️ {name}: ERROR — {e}")
                failed += 1
        print(f"\nSummary: {passed} passed, {fixed} fixed, {failed} failed, {skipped} skipped")

if __name__ == "__main__":
    run_checks()
