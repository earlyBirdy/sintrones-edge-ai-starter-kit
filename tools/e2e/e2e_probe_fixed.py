#!/usr/bin/env python3
"""Probe the same queries the tabs use, against the canonical DB path."""
from pathlib import Path
import os, sqlite3

REPO_ROOT = Path.cwd()
DB_PATH = Path(os.getenv("EDGE_DB_PATH") or (REPO_ROOT / "data" / "edgekit.db"))
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def q(con, sql):
    try:
        return con.execute(sql).fetchall()
    except Exception as e:
        return f"ERROR: {e}"

def main():
    con = sqlite3.connect(DB_PATH); con.row_factory = sqlite3.Row
    checks = {
        "Yield & Quality": "SELECT date(ts) d, SUM(result='PASS') pass_cnt, SUM(result='FAIL') fail_cnt FROM inspections GROUP BY date(ts) ORDER BY d DESC LIMIT 7",
        "Fleet": "SELECT device_id, COUNT(*) event_cnt FROM events GROUP BY device_id ORDER BY event_cnt DESC",
        "Data Traceability": "SELECT unit_id, station, result, score, ts FROM inspections ORDER BY ts DESC LIMIT 10",
        "Benchmark Matrix": "SELECT COALESCE(engine, model) engine, input_size, ROUND(AVG(fps),1) fps, ROUND(AVG(latency_ms),1) latency_ms, ROUND(AVG(accuracy),2) acc FROM benchmarks GROUP BY 1,2",
        "Log Viewer": "SELECT ts, severity, type, message FROM events ORDER BY ts DESC LIMIT 10",
        "Health Check": "SELECT COUNT(*) devices FROM devices"
    }
    print(f"Probing DB: {DB_PATH}")
    for name, sql in checks.items():
        rows = q(con, sql)
        print(f"\n== {name} ==")
        if isinstance(rows, str): print(rows)
        else:
            for r in rows[:5]: print(dict(r))

if __name__ == "__main__":
    main()
