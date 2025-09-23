#!/usr/bin/env python3
# e2e_bootstrap_pipeline_v3.py
# Schema-aware bootstrap that adapts to your existing columns and NOT NULL constraints.
from __future__ import annotations
import os, sqlite3, json, random
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path.cwd()
DATA = ROOT / "data"; DATA.mkdir(exist_ok=True)
DB_PATH = Path(os.getenv("EDGE_DB_PATH") or (DATA / "edgekit.db"))

def connect():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA journal_mode=WAL;")
    con.row_factory = sqlite3.Row
    return con

def table_cols(con, table):
    cur = con.execute(f"PRAGMA table_info({table});")
    # returns list of dicts: name, notnull, dflt
    return [{ "name": r[1], "notnull": int(r[3])==1, "dflt": r[4] } for r in cur.fetchall()]

def ensure_min_schema(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS devices (id INTEGER PRIMARY KEY AUTOINCREMENT, device_id TEXT UNIQUE NOT NULL, model TEXT, location TEXT);
    CREATE TABLE IF NOT EXISTS sensor_readings (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, device_id TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS quality_results (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, device_id TEXT NOT NULL, reading_id INTEGER NOT NULL, passed INTEGER NOT NULL, defect_code TEXT);
    CREATE TABLE IF NOT EXISTS inspections (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, unit_id TEXT NOT NULL, station TEXT, result TEXT NOT NULL, score REAL);
    CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, device_id TEXT NOT NULL, type TEXT, message TEXT);
    CREATE TABLE IF NOT EXISTS event_log (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, level TEXT NOT NULL, source TEXT NOT NULL, message TEXT NOT NULL, kv JSON);
    CREATE TABLE IF NOT EXISTS benchmarks (id INTEGER PRIMARY KEY AUTOINCREMENT, engine TEXT NOT NULL, input_size TEXT NOT NULL, fps REAL, latency_ms REAL, accuracy REAL);
    CREATE TABLE IF NOT EXISTS anomalies (id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL, device_id TEXT NOT NULL, severity TEXT, note TEXT);
    """)
    con.commit()

def col_exists(cols, name): return any(c["name"]==name for c in cols)
def wants(cols, name): return col_exists(cols, name)
def required(cols, name): 
    for c in cols:
        if c["name"]==name: return c["notnull"] and c["dflt"] is None
    return False

def seed_devices(con):
    rows=[("edgecam-01","Jetson Orin","Line A"),("edgecam-02","Jetson Orin","Line B"),("edgecam-03","RTX A2000","Line C"),("edgecam-04","iGPU","Rework"),("edgecam-05","CPU","Lab")]
    for r in rows:
        con.execute("INSERT OR IGNORE INTO devices(device_id,model,location) VALUES(?,?,?)", r)
    con.commit()

def insert_row(con, table, values: dict):
    cols = table_cols(con, table)
    # Fill required NOT NULLs with defaults if missing
    for c in cols:
        n = c["name"]
        if n in ("id",): continue
        if n not in values and c["notnull"] and c["dflt"] is None:
            # supply sensible defaults by column name
            if n in ("device_id","unit_id"): values[n] = values.get("device_id","edgecam-01")
            elif n in ("ts",): values[n] = datetime.utcnow().isoformat()
            elif n in ("station",): values[n] = None
            elif n in ("result",): values[n] = "PASS"
            elif n in ("score","value","fps","latency_ms","accuracy"): values[n] = 0
            elif n in ("severity","level"): values[n] = "INFO"
            elif n in ("type",): values[n] = "heartbeat"
            elif n in ("message",): values[n] = "seed"
            elif n in ("meta_json","kv"): values[n] = "{}"
            elif n in ("engine",): values[n] = "yolo-v8.2"
            elif n in ("input_size",): values[n] = "640x640"
            elif n in ("model","model_ver"): values[n] = "v1"
            elif n in ("defect_tag",): values[n] = None
            elif n in ("reading_id",): values[n] = 0
            elif n in ("sensor_type",): values[n] = values.get("metric","temp")
            elif n in ("unit",): values[n] = "unit"
            elif n in ("passed",): values[n] = 1
            else: values[n] = None
    keys = [k for k in values.keys() if col_exists(cols, k)]
    placeholders = ",".join("?" for _ in keys)
    sql = f"INSERT INTO {table}({','.join(keys)}) VALUES({placeholders})"
    con.execute(sql, tuple(values[k] for k in keys))

def seed_everything(con, total=500):
    dcols = table_cols(con,"devices")
    sr_cols = table_cols(con,"sensor_readings")
    qr_cols = table_cols(con,"quality_results")
    in_cols = table_cols(con,"inspections")
    ev_cols = table_cols(con,"events")
    el_cols = table_cols(con,"event_log")
    bm_cols = table_cols(con,"benchmarks")
    an_cols = table_cols(con,"anomalies")

    devs = [r[0] for r in con.execute("SELECT device_id FROM devices").fetchall()]
    if not devs:
        devs = ["edgecam-01"]

    t0 = datetime.utcnow() - timedelta(hours=48)
    metrics = [("temp","temperature","C"), ("vibration","vibration","g"), ("current","current","A")]

    for i in range(total):
        ts = (t0 + timedelta(seconds=i*60))
        ts_iso = ts.isoformat() if i % 10 == 0 else ts.strftime("%Y-%m-%d %H:%M:%S")
        dev = random.choice(devs)
        metric, sensor_type, unit = random.choice(metrics)
        val = round(random.uniform(0.1,1.5),3)

        # sensor_readings
        sr = {"ts": ts_iso, "device_id": dev}
        if wants(sr_cols,"metric"): sr["metric"]=metric
        if wants(sr_cols,"sensor_type"): sr["sensor_type"]=sensor_type
        if wants(sr_cols,"unit"): sr["unit"]=unit
        if wants(sr_cols,"value"): sr["value"]=val
        insert_row(con, "sensor_readings", sr)
        rid = con.execute("SELECT last_insert_rowid()").fetchone()[0]

        # quality_results
        passed = 0 if random.random() < 0.086 else 1
        defect = random.choice([None,"scratch","misalign","overheat"]) if not passed else None
        qr = {"ts": ts_iso, "device_id": dev, "reading_id": rid, "passed": passed, "defect_code": defect}
        insert_row(con, "quality_results", qr)

        # inspections
        unit_id = f"U{i:05d}" if i % 2 == 0 else f"R{i:05d}"
        result = "PASS" if passed else "FAIL"
        score = 0.95 if passed else 0.85
        ins = {"ts": ts_iso, "unit_id": unit_id, "result": result, "score": score, "device_id": dev}
        if wants(in_cols,"defect_tag"): ins["defect_tag"] = defect
        if wants(in_cols,"model_ver"): ins["model_ver"] = "v1"
        insert_row(con, "inspections", ins)

        # events every 60 rows
        if i % 60 == 0:
            ev = {"ts": ts_iso, "device_id": dev, "type": "heartbeat", "message": "device alive", "severity": "INFO", "meta_json": "{}"}
            insert_row(con, "events", ev)

        # anomalies for some failures
        if not passed and i % 3 == 0:
            an = {"ts": ts_iso, "device_id": dev, "severity": "HIGH", "note": "auto-seeded"}
            if wants(an_cols,"reading_id"): an["reading_id"] = rid
            insert_row(con, "anomalies", an)

        # event_log heartbeat
        if i % 120 == 0:
            el = {"ts": ts_iso, "level": "INFO", "source": "e2e_bootstrap_v3", "message": "seed", "kv": "{}"}
            insert_row(con, "event_log", el)

    # benchmarks
    for r in [("yolo-v8.2","640x640",45.2,22.1,0.91),("seg-v1.0","512x512",60.1,16.4,0.88)]:
        bm = {"engine": r[0], "input_size": r[1], "fps": r[2], "latency_ms": r[3]}
        # table may use 'accuracy' or 'acc'
        if col_exists(bm_cols,"accuracy"):
            bm["accuracy"] = r[4]
        elif col_exists(bm_cols,"acc"):
            bm["acc"] = r[4]
        # optional extra cols
        bm["ts"] = datetime.utcnow().isoformat() if col_exists(bm_cols,"ts") else bm.get("ts")
        bm["device_id"] = devs[0] if col_exists(bm_cols,"device_id") else bm.get("device_id")
        bm["model"] = r[0] if col_exists(bm_cols,"model") else bm.get("model")
        bm["notes"] = "seed" if col_exists(bm_cols,"notes") else bm.get("notes")
        insert_row(con, "benchmarks", bm)

def ensure_filesystem():
    (ROOT/"logs/anomalies").mkdir(parents=True, exist_ok=True)
    (ROOT/"benchmarks").mkdir(exist_ok=True)
    (ROOT/"xai_results").mkdir(exist_ok=True)
    (ROOT/"pipelines").mkdir(exist_ok=True)
    (ROOT/"examples").mkdir(exist_ok=True)
    for p in ["models/fewshot","models/finetune","models/packs","config/connectors"]:
        (ROOT/p).mkdir(parents=True, exist_ok=True)
    (ROOT/"config/inspection_rules.yaml").write_text("rules:\n  - name: default\n    threshold: 0.5\n", encoding="utf-8")
    (ROOT/"config/cameras.yaml").write_text("cameras:\n  - id: cam0\n    url: rtsp://example\n", encoding="utf-8")
    (ROOT/"config/policy.yaml").write_text("governance:\n  allow_export: true\n", encoding="utf-8")
    (ROOT/"logs/anomaly_log.csv").write_text("ts,severity,type,message\n", encoding="utf-8")
    (ROOT/"logs/app.log").write_text("2025-09-22 10:00:00 Boot\n", encoding="utf-8")
    (ROOT/"logs/app.jsonl").write_text('{"ts":"2025-09-22T10:00:00","sev":"INFO","msg":"hello"}\n', encoding="utf-8")
    (ROOT/"mes_latest.csv").write_text("unit_id,result,score,ts\nU0001,PASS,0.98,2025-09-22 10:00:00\n", encoding="utf-8")

def gen_anomaly_images(n=24):
    try:
        from PIL import Image, ImageDraw
    except Exception:
        return
    folder = ROOT/"logs/anomalies"
    for i in range(n):
        img = Image.new("RGB", (160,120), (200, 80+i*5, 80))
        d = ImageDraw.Draw(img); d.text((10, 50), f"anom {i}", fill=(255,255,255))
        img.save(folder/f"anom_{i:04d}.png")

def main():
    print(f"Using DB: {DB_PATH}")
    con = connect()
    ensure_min_schema(con)
    seed_devices(con)
    seed_everything(con, total=500)
    ensure_filesystem()
    gen_anomaly_images(24)
    con.commit()
    print("Bootstrap v3 complete.")
if __name__ == "__main__":
    main()
