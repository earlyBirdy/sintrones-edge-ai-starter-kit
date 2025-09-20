#!/usr/bin/env python3
"""
Data Flow Probe for Sintrones Edge AI Starter Kit
- Creates/repairs a minimal SQLite schema
- Seeds synthetic sensor + inference + anomaly data
- Verifies read paths and returns KPIs used by several Streamlit tabs
- Usable as CLI or as an import (for a diagnostics page)

Default DB: ./data/edgekit.db (SQLite)
Override with EDGEKIT_DB_PATH=/absolute/or/relative/path.sqlite
"""

from __future__ import annotations
import os
import json
import random
import sqlite3
import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional


# ----------------------------
# Config
# ----------------------------

DEFAULT_DB_PATH = os.getenv("EDGEKIT_DB_PATH", "data/edgekit.db")
RANDOM_SEED = 42
random.seed(RANDOM_SEED)


# ----------------------------
# Schema (minimal, non-breaking)
# ----------------------------
SCHEMA_SQL = [
    """
    CREATE TABLE IF NOT EXISTS devices (
        device_id TEXT PRIMARY KEY,
        model TEXT,
        location TEXT,
        first_seen_ts TEXT,
        last_seen_ts TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS sensor_readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        device_id TEXT NOT NULL,
        sensor_type TEXT NOT NULL,
        value REAL NOT NULL,
        unit TEXT,
        FOREIGN KEY(device_id) REFERENCES devices(device_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS inference_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        device_id TEXT NOT NULL,
        reading_id INTEGER NOT NULL,
        model_name TEXT NOT NULL,
        pred_label TEXT,
        pred_score REAL,
        FOREIGN KEY(device_id) REFERENCES devices(device_id),
        FOREIGN KEY(reading_id) REFERENCES sensor_readings(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS anomalies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        device_id TEXT NOT NULL,
        reading_id INTEGER NOT NULL,
        severity TEXT CHECK(severity IN ('low','medium','high')) NOT NULL,
        note TEXT,
        FOREIGN KEY(device_id) REFERENCES devices(device_id),
        FOREIGN KEY(reading_id) REFERENCES sensor_readings(id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS quality_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        device_id TEXT NOT NULL,
        reading_id INTEGER NOT NULL,
        passed INTEGER NOT NULL CHECK(passed IN (0,1)),
        defect_code TEXT,
        FOREIGN KEY(device_id) REFERENCES devices(device_id),
        FOREIGN KEY(reading_id) REFERENCES sensor_readings(id)
    );
    """,
    # helpful for a Log/Traceability tab
    """
    CREATE TABLE IF NOT EXISTS event_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        level TEXT NOT NULL,
        source TEXT NOT NULL,
        message TEXT NOT NULL,
        kv JSON
    );
    """
]


# ----------------------------
# Dataclasses for report
# ----------------------------

@dataclass
class KpiReport:
    total_devices: int
    active_devices_24h: int
    total_readings: int
    total_inferences: int
    total_anomalies: int
    total_quality_checks: int
    yield_rate_pct: float
    last_ingest_ts: Optional[str]
    sample_devices: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ----------------------------
# DB helpers
# ----------------------------

def _ensure_dirs(db_path: str) -> None:
    p = Path(db_path)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)

def get_conn(db_path: str) -> sqlite3.Connection:
    _ensure_dirs(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def migrate(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    for sql in SCHEMA_SQL:
        cur.execute(sql)
    conn.commit()


# ----------------------------
# Seeders (synthetic E2E)
# ----------------------------

DEVICE_MODELS = ["SIN-Q670", "SIN-R680", "SIN-J6412"]
SENSOR_TYPES = ["temperature", "vibration", "voltage", "current"]
UNITS = {"temperature": "°C", "vibration": "g", "voltage": "V", "current": "A"}

def _upsert_device(conn: sqlite3.Connection, device_id: str, model: str, location: str, ts: str) -> None:
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO devices (device_id, model, location, first_seen_ts, last_seen_ts)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(device_id) DO UPDATE SET
            model=excluded.model,
            location=excluded.location,
            last_seen_ts=excluded.last_seen_ts;
    """, (device_id, model, location, ts, ts))
    conn.commit()

def seed_data(conn: sqlite3.Connection, n_devices: int = 5, readings_per_device: int = 100,
              start_minutes_ago: int = 180, model_name: str = "edgekit-demo-v1") -> None:
    """
    Generate devices, sensor readings, inference events, anomalies, and quality results.
    """
    base_ts = datetime.utcnow() - timedelta(minutes=start_minutes_ago)
    cur = conn.cursor()

    # Devices
    device_ids = [f"EDGEKIT-{i:03d}" for i in range(1, n_devices + 1)]
    for did in device_ids:
        model = random.choice(DEVICE_MODELS)
        location = random.choice(["Line-A", "Line-B", "Line-C", "Field-East", "Depot-3"])
        _upsert_device(conn, did, model, location, base_ts.isoformat())

    # Readings + Inference + Anomalies + Quality
    for did in device_ids:
        ts = base_ts
        last_reading_id = None
        for _ in range(readings_per_device):
            ts += timedelta(seconds=random.randint(10, 40))
            sensor_type = random.choice(SENSOR_TYPES)
            # synthetic sensor values
            val = {
                "temperature": random.gauss(55, 6),
                "vibration": abs(random.gauss(0.35, 0.1)),
                "voltage": random.gauss(24, 0.8),
                "current": abs(random.gauss(2.0, 0.5))
            }[sensor_type]

            cur.execute("""
                INSERT INTO sensor_readings (ts, device_id, sensor_type, value, unit)
                VALUES (?, ?, ?, ?, ?)
            """, (ts.isoformat(), did, sensor_type, float(val), UNITS[sensor_type]))
            reading_id = cur.lastrowid

            # Inference simulation
            pred_label = "ok"
            score = round(random.uniform(0.85, 0.999), 3)

            # Occasionally flip to "defect" with lower score
            if random.random() < 0.08:
                pred_label = "defect"
                score = round(random.uniform(0.55, 0.8), 3)

            cur.execute("""
                INSERT INTO inference_events (ts, device_id, reading_id, model_name, pred_label, pred_score)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (ts.isoformat(), did, reading_id, model_name, pred_label, score))

            # Anomaly only when defect-ish or extreme sensor
            is_anomaly = pred_label == "defect" or (
                sensor_type == "temperature" and val > 70
            ) or (
                sensor_type == "vibration" and val > 0.7
            )
            if is_anomaly and random.random() < 0.75:
                sev = random.choices(["low", "medium", "high"], weights=[4, 3, 1])[0]
                cur.execute("""
                    INSERT INTO anomalies (ts, device_id, reading_id, severity, note)
                    VALUES (?, ?, ?, ?, ?)
                """, (ts.isoformat(), did, reading_id, sev, f"auto-flag: {sensor_type}={val:.2f}"))

            # Quality check (pass/fail)
            passed = 1 if pred_label == "ok" and random.random() < 0.97 else 0
            defect_code = None if passed else random.choice(["D-OVRHEAT", "D-VIB-THR", "D-LOWV", "D-OVRCUR"])
            cur.execute("""
                INSERT INTO quality_results (ts, device_id, reading_id, passed, defect_code)
                VALUES (?, ?, ?, ?, ?)
            """, (ts.isoformat(), did, reading_id, passed, defect_code))

            last_reading_id = reading_id

        # Update last_seen
        cur.execute("UPDATE devices SET last_seen_ts=? WHERE device_id=?", (ts.isoformat(), did))

    # Log an event
    cur.execute("""
        INSERT INTO event_log (ts, level, source, message, kv)
        VALUES (?, 'INFO', 'data_flow_probe', 'Seed complete', ?)
    """, (datetime.utcnow().isoformat(), json.dumps({"n_devices": n_devices, "rpd": readings_per_device})))

    conn.commit()


# ----------------------------
# Readers / KPI builders
# ----------------------------

def _fetch_one(conn: sqlite3.Connection, sql: str, params: Tuple = ()) -> Any:
    cur = conn.cursor()
    cur.execute(sql, params)
    row = cur.fetchone()
    return row[0] if row else None

def build_kpis(conn: sqlite3.Connection) -> KpiReport:
    total_devices = _fetch_one(conn, "SELECT COUNT(*) FROM devices") or 0
    active_devices_24h = _fetch_one(conn, """
        SELECT COUNT(*) FROM devices
        WHERE last_seen_ts >= datetime('now', '-1 day')
    """) or 0

    total_readings = _fetch_one(conn, "SELECT COUNT(*) FROM sensor_readings") or 0
    total_inferences = _fetch_one(conn, "SELECT COUNT(*) FROM inference_events") or 0
    total_anomalies = _fetch_one(conn, "SELECT COUNT(*) FROM anomalies") or 0
    total_quality = _fetch_one(conn, "SELECT COUNT(*) FROM quality_results") or 0

    passed = _fetch_one(conn, "SELECT COUNT(*) FROM quality_results WHERE passed=1") or 0
    yield_rate = (passed / total_quality * 100.0) if total_quality else 0.0

    last_ingest_ts = _fetch_one(conn, "SELECT MAX(ts) FROM sensor_readings")
    sample_devices = []
    cur = conn.cursor()
    cur.execute("SELECT device_id FROM devices ORDER BY device_id LIMIT 5")
    sample_devices = [r[0] for r in cur.fetchall()]

    return KpiReport(
        total_devices=total_devices,
        active_devices_24h=active_devices_24h,
        total_readings=total_readings,
        total_inferences=total_inferences,
        total_anomalies=total_anomalies,
        total_quality_checks=total_quality,
        yield_rate_pct=round(yield_rate, 2),
        last_ingest_ts=last_ingest_ts,
        sample_devices=sample_devices
    )


# ----------------------------
# Public API
# ----------------------------

def run_probe(db_path: str = DEFAULT_DB_PATH,
              reset: bool = False,
              n_devices: int = 5,
              readings_per_device: int = 100) -> Dict[str, Any]:
    """
    Runs migration, optional reset, seeds (if empty), and returns KPIs.
    """
    _ensure_dirs(db_path)
    conn = get_conn(db_path)

    if reset and Path(db_path).exists():
        conn.close()
        os.remove(db_path)
        conn = get_conn(db_path)

    migrate(conn)

    # If DB empty, seed; else just verify and summarize
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sensor_readings;")
    empty = (cur.fetchone() or [0])[0] == 0

    if empty:
        seed_data(conn, n_devices=n_devices, readings_per_device=readings_per_device)

    kpis = build_kpis(conn)

    report = {
        "db_path": str(Path(db_path).resolve()),
        "reset": reset,
        "seeded_on_empty": empty,
        "kpis": kpis.to_dict(),
    }
    return report


# ----------------------------
# CLI
# ----------------------------

def main():
    parser = argparse.ArgumentParser(description="Sintrones Edge AI Starter Kit - Data Flow Probe")
    parser.add_argument("--db", dest="db_path", default=DEFAULT_DB_PATH, help="SQLite DB path (default: data/edgekit.db)")
    parser.add_argument("--reset", action="store_true", help="Delete DB and re-create schema before seeding")
    parser.add_argument("--devices", type=int, default=5, help="Number of synthetic devices to seed when empty/reset")
    parser.add_argument("--readings", type=int, default=100, help="Readings per device to seed when empty/reset")
    parser.add_argument("--print", dest="print_report", action="store_true", help="Print JSON report to stdout")
    args = parser.parse_args()

    rpt = run_probe(db_path=args.db_path, reset=args.reset, n_devices=args.devices, readings_per_device=args.readings)

    if args.print_report:
        print(json.dumps(rpt, indent=2))

if __name__ == "__main__":
    main()
