#!/usr/bin/env python3
import argparse, json, os, sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DEF_DB = os.getenv("EDGEKIT_DB_PATH", "data/edgekit.db")
DEF_EXPORT_DIR = os.getenv("MES_EXPORT_DIR", "exports/mes")
LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "24"))

def conn(db):
    c = sqlite3.connect(db)
    c.row_factory = sqlite3.Row
    return c

def count(c, sql, params=()):
    return c.execute(sql, params).fetchone()[0]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=DEF_DB)
    ap.add_argument("--export_dir", default=DEF_EXPORT_DIR)
    ap.add_argument("--hours", type=int, default=LOOKBACK_HOURS)
    ap.add_argument("--print", action="store_true", dest="p")
    args = ap.parse_args()

    now = datetime.utcnow()
    lookback = now - timedelta(hours=args.hours)

    out = {
        "db_path": str(Path(args.db).resolve()),
        "export_dir": str(Path(args.export_dir).resolve()),
        "lookback_hours": args.hours,
        "db": {},
        "exports": {},
        "parity": {}
    }

    with conn(args.db) as c:
        # DB coverage in lookback
        out["db"]["readings_24h"]  = count(c, "SELECT COUNT(*) FROM sensor_readings WHERE ts >= datetime('now', ?)", (f"-{args.hours} hours",))
        out["db"]["infer_24h"]     = count(c, "SELECT COUNT(*) FROM inference_events WHERE ts >= datetime('now', ?)", (f"-{args.hours} hours",))
        out["db"]["quality_24h"]   = count(c, "SELECT COUNT(*) FROM quality_results WHERE ts >= datetime('now', ?)", (f"-{args.hours} hours",))
        out["db"]["anomalies_24h"] = count(c, "SELECT COUNT(*) FROM anomalies WHERE ts >= datetime('now', ?)", (f"-{args.hours} hours",))

        # Orphans
        out["db"]["orphans_no_infer"] = count(c, """
            SELECT COUNT(*) FROM sensor_readings r
            LEFT JOIN inference_events ie ON ie.reading_id=r.id
            WHERE r.ts >= datetime('now', ?) AND ie.reading_id IS NULL
        """, (f"-{args.hours} hours",))
        out["db"]["orphans_no_quality"] = count(c, """
            SELECT COUNT(*) FROM inference_events ie
            LEFT JOIN quality_results q ON q.reading_id=ie.reading_id
            WHERE ie.ts >= datetime('now', ?) AND q.reading_id IS NULL
        """, (f"-{args.hours} hours",))

    # Exports side (very simple heuristic: count files & newest mtime)
    exp_dir = Path(args.export_dir)
    if exp_dir.exists():
        files = sorted(exp_dir.glob("*"))
        out["exports"]["file_count"] = len(files)
        out["exports"]["latest_file"] = files[-1].name if files else None
        out["exports"]["latest_mtime"] = (
            datetime.utcfromtimestamp(files[-1].stat().st_mtime).isoformat() + "Z"
            if files else None
        )
    else:
        out["exports"]["file_count"] = 0
        out["exports"]["latest_file"] = None
        out["exports"]["latest_mtime"] = None

    # Parity heuristics
    out["parity"]["db_has_data_last_24h"] = any([
        out["db"]["readings_24h"],
        out["db"]["infer_24h"],
        out["db"]["quality_24h"],
        out["db"]["anomalies_24h"],
    ])
    out["parity"]["exports_exist"] = out["exports"]["file_count"] > 0

    # Suggestion
    if out["parity"]["db_has_data_last_24h"] and not out["parity"]["exports_exist"]:
        out["parity"]["hint"] = "DB has fresh data but exports/mes is empty — check your MES/export step."
    elif not out["parity"]["db_has_data_last_24h"]:
        out["parity"]["hint"] = "No fresh DB data in the last 24h — the UI may look empty due to lookback filters."
    else:
        out["parity"]["hint"] = "DB and exports appear present. If UI is wrong, check device IDs/timestamps and tab lookback."

    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
