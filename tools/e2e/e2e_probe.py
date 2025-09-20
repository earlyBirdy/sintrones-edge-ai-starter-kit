#!/usr/bin/env python3
"""E2E probe: verify queries that Streamlit tabs use can return data.
Run after generate_dummy_data.py
"""
from pathlib import Path
import sqlite3, pandas as pd, json

REPO_ROOT = Path("/mnt/data/sintrones_edge_ai_kit_0920/sintrones-edge-ai-starter-kit-main")
DB_PATH = REPO_ROOT / "data" / "edge.db"

def q(con, sql):
    try:
        return con.execute(sql).fetchall()
    except Exception as e:
        return f"ERROR: {e}"

def main():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    checks = {
        "Yield & Quality": "SELECT date(ts) as d, SUM(result='PASS') as pass_cnt, SUM(result='FAIL') as fail_cnt FROM inspections GROUP BY date(ts) ORDER BY d DESC LIMIT 7",
        "Fleet": "SELECT device_id, COUNT(*) as event_cnt FROM events GROUP BY device_id ORDER BY event_cnt DESC",
        "Data Traceability": "SELECT unit_id, station, result, score, ts FROM inspections ORDER BY ts DESC LIMIT 10",
        "Benchmark Matrix": "SELECT model, input_size, ROUND(AVG(fps),1) fps, ROUND(AVG(latency_ms),1) latency_ms, ROUND(AVG(accuracy),2) acc FROM benchmarks GROUP BY model, input_size",
        "Log Viewer": "SELECT ts, severity, type, message FROM events ORDER BY ts DESC LIMIT 10",
        "Health Check": "SELECT COUNT(*) FROM devices"
    }

    for name, sql in checks.items():
        rows = q(con, sql)
        if isinstance(rows, str):
            print(f"[{name}] {rows}")
        else:
            print(f"\n== {name} ==")
            for r in rows[:5]:
                print(dict(r))

if __name__ == "__main__":
    main()
