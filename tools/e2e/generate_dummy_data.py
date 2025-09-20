#!/usr/bin/env python3
"""Seed the local SQLite DB with realistic dummy data that exercises the Streamlit tabs.
Assumes repo root layout like:
  /mnt/data/sintrones_edge_ai_kit_0920/sintrones-edge-ai-starter-kit-main
and DB at data/edge.db.
"""
from __future__ import annotations
from pathlib import Path
import sqlite3, json, random, time, datetime as dt

REPO_ROOT = Path("/mnt/data/sintrones_edge_ai_kit_0920/sintrones-edge-ai-starter-kit-main")
DB_PATH = REPO_ROOT / "data" / "edge.db"
SCHEMA_SQL = (REPO_ROOT / "core" / "schema.sql").read_text(encoding="utf-8", errors="ignore")

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def migrate(con: sqlite3.Connection):
    # schema.sql in this repo uses ellipses in this copy, so we minimally make a working schema here.
    # If your schema.sql is complete locally, this call will still succeed for existing tables.
    con.executescript("""
    PRAGMA journal_mode=WAL;
    PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS devices (
        device_id TEXT PRIMARY KEY,
        name TEXT,
        site TEXT,
        model TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE IF NOT EXISTS sensor_readings (
        ts TEXT,
        device_id TEXT,
        sensor_id TEXT,
        metric TEXT,
        value REAL,
        raw_json TEXT,
        PRIMARY KEY (ts, device_id, sensor_id, metric)
    );
    CREATE INDEX IF NOT EXISTS idx_sensor_t ON sensor_readings(ts);
    CREATE INDEX IF NOT EXISTS idx_sensor_dev ON sensor_readings(device_id, sensor_id);

    CREATE TABLE IF NOT EXISTS inspections (
        ts TEXT,
        device_id TEXT,
        unit_id TEXT,
        station TEXT,
        result TEXT,
        score REAL,
        defect_tag TEXT,
        model_ver TEXT,
        PRIMARY KEY (ts, device_id, unit_id)
    );
    CREATE INDEX IF NOT EXISTS idx_insp_lookup ON inspections(unit_id, station, ts);

    CREATE TABLE IF NOT EXISTS benchmarks (
        ts TEXT,
        device_id TEXT,
        model TEXT,
        input_size TEXT,
        fps REAL,
        latency_ms REAL,
        accuracy REAL,
        notes TEXT
    );

    CREATE TABLE IF NOT EXISTS events (
        ts TEXT,
        device_id TEXT,
        severity TEXT,
        type TEXT,
        message TEXT,
        meta_json TEXT
    );

    CREATE TABLE IF NOT EXISTS changes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT DEFAULT CURRENT_TIMESTAMP,
        table_name TEXT,
        op TEXT,
        pk TEXT,
        row_json TEXT
    );
    """)

def seed_devices(con):
    devices = [
        ("EDGE-01","Line A Camera","TH-BKK","A5000"),
        ("EDGE-02","Line B Camera","TH-BKK","A5000"),
        ("GATE-01","Gateway Node","TH-BKK","AGX")
    ]
    con.executemany("INSERT OR IGNORE INTO devices(device_id,name,site,model) VALUES (?,?,?,?)", devices)

def seed_sensor_readings(con, hours=24):
    now = dt.datetime.utcnow()
    for dev in ("EDGE-01","EDGE-02"):
        for h in range(hours*6):  # ~10-min cadence
            ts = (now - dt.timedelta(minutes=10*h)).strftime("%Y-%m-%d %H:%M:%S")
            temp = 40 + random.random()*10
            vib = 0.01 + random.random()*0.1
            con.execute("INSERT OR REPLACE INTO sensor_readings VALUES (?,?,?,?,?,?)",
                        (ts, dev, "temp", "C", temp, json.dumps({{"src":"sim"}})))
            con.execute("INSERT OR REPLACE INTO sensor_readings VALUES (?,?,?,?,?,?)",
                        (ts, dev, "vibration", "g", vib, json.dumps({{"src":"sim"}})))

def seed_inspections(con, hours=24, pass_rate=0.94):
    now = dt.datetime.utcnow()
    for dev in ("EDGE-01","EDGE-02"):
        for i in range(hours*20):
            ts = (now - dt.timedelta(minutes=3*i)).strftime("%Y-%m-%d %H:%M:%S")
            unit = f"U{{int(time.time())%100000:05d}}{{i:03d}}"
            station = random.choice(["ST01","ST02","ST03"])
            ok = random.random() < pass_rate
            result = "PASS" if ok else "FAIL"
            score = round(random.uniform(0.6, 0.99), 3)
            defect = None if ok else random.choice(["scratch","chip","missing"])
            model_ver = random.choice(["yolo-v8.1","yolo-v8.2","seg-v1.0"])
            con.execute("INSERT OR REPLACE INTO inspections VALUES (?,?,?,?,?,?,?,?)",
                        (ts, dev, unit, station, result, score, defect, model_ver))

def seed_benchmarks(con):
    now = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    rows = [
        (now,"EDGE-01","yolo-v8.2","640x640",45.2, 22.1, 0.91, "INT8 TRT"),
        (now,"EDGE-02","seg-v1.0","512x512",60.1, 16.4, 0.88, "FP16 TRT"),
    ]
    con.executemany("INSERT INTO benchmarks VALUES (?,?,?,?,?,?,?,?)", rows)

def seed_events(con):
    now = dt.datetime.utcnow()
    rows = []
    for i in range(20):
        ts = (now - dt.timedelta(minutes=15*i)).strftime("%Y-%m-%d %H:%M:%S")
        rows.append((ts,"EDGE-01","INFO","heartbeat","device ok", json.dumps({{"tick":i}})))
    rows.append((now.strftime("%Y-%m-%d %H:%M:%S"), "EDGE-02","WARN","low_fps","FPS dropped below threshold", json.dumps({{"fps":37}})))
    con.executemany("INSERT INTO events VALUES (?,?,?,?,?,?)", rows)

def main():
    con = connect()
    migrate(con)
    seed_devices(con)
    seed_sensor_readings(con, hours=24)
    seed_inspections(con, hours=24)
    seed_benchmarks(con)
    seed_events(con)
    con.commit()
    print(f"Seeded dummy data into {{DB_PATH}}")

if __name__ == "__main__":
    main()
