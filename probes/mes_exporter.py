#!/usr/bin/env python3
"""
MES exporter (schema-aware)
- Exports last N hours of joined readings → inference → quality → anomalies
- Auto-detects optional columns (e.g., inference_events.score, anomalies.severity)
- Writes timestamped CSV/JSON and "latest" copies in exports/mes
"""

import os
import csv
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB = os.getenv("EDGEKIT_DB_PATH", "data/edgekit.db")
OUT_DIR = Path(os.getenv("MES_EXPORT_DIR", "exports/mes"))

def _has_col(conn: sqlite3.Connection, table: str, column: str) -> bool:
    cur = conn.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())  # row[1] = name

def _build_sql(conn: sqlite3.Connection) -> str:
    # Optional columns
    has_ie_score   = _has_col(conn, "inference_events", "score")
    has_a_severity = _has_col(conn, "anomalies", "severity")

    # Always-present fields
    selects = [
        "r.id              AS reading_id",
        "r.device_id       AS device_id",
        "r.ts              AS reading_ts",  # UTC
        "ie.pred_label     AS pred_label",
        "q.passed          AS quality_passed",
    ]

    # Optional fields with NULL fallback
    selects.append(("ie.score AS pred_score") if has_ie_score else ("NULL AS pred_score"))
    selects.append(("a.severity AS anomaly_severity") if has_a_severity else ("NULL AS anomaly_severity"))

    sql = f"""
    SELECT
      {", ".join(selects)}
    FROM sensor_readings r
    LEFT JOIN inference_events ie ON ie.reading_id = r.id
    LEFT JOIN quality_results  q  ON q.reading_id  = r.id
    LEFT JOIN anomalies        a  ON a.reading_id  = r.id
    WHERE r.ts >= datetime('now', ?)
    ORDER BY r.ts DESC
    """
    return sql

def run_export(hours: int = 24) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    h = f"-{hours} hours"

    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    sql = _build_sql(con)
    rows = con.execute(sql, (h,)).fetchall()
    con.close()

    ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    base = f"mes_last{hours}h_{ts}"
    csv_path = OUT_DIR / f"{base}.csv"
    json_path = OUT_DIR / f"{base}.json"
    latest_csv = OUT_DIR / "mes_latest.csv"
    latest_json = OUT_DIR / "mes_latest.json"

    # CSV
    headers = rows[0].keys() if rows else [
        "reading_id", "device_id", "reading_ts",
        "pred_label", "quality_passed", "pred_score", "anomaly_severity"
    ]
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(dict(r))

    # JSON
    with json_path.open("w") as f:
        json.dump([dict(r) for r in rows], f, indent=2)

    # "latest" copies (atomic replace)
    latest_csv.write_bytes(csv_path.read_bytes())
    latest_json.write_bytes(json_path.read_bytes())

    return {
        "rows": len(rows),
        "csv": str(csv_path),
        "json": str(json_path),
        "latest_csv": str(latest_csv),
        "latest_json": str(latest_json),
    }

if __name__ == "__main__":
    hrs = int(os.getenv("LOOKBACK_HOURS", "24"))
    info = run_export(hrs)
    print(json.dumps(info, indent=2))
