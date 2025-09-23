#!/usr/bin/env python3
# tab_health_probe.py
# Verifies data/assets that each of the 19 tabs rely on.
import os, sqlite3, json
from pathlib import Path

ROOT = Path.cwd()
DB = Path(os.getenv("EDGE_DB_PATH") or (ROOT / "data" / "edgekit.db"))

def q(con, sql):
    try:
        return con.execute(sql).fetchone()[0]
    except Exception as e:
        return f"ERR: {e}"

def exists(p): return "OK" if Path(p).exists() else "MISS"

def main():
    print(f"DB: {DB} ({'exists' if DB.exists() else 'missing'})")
    con = sqlite3.connect(DB) if DB.exists() else None

    # SQL-backed tabs
    if con:
        print('\n[SQL] Yield & Quality / Traceability (inspections) =>', q(con, "SELECT COUNT(*) FROM inspections"))
        print('[SQL] Fleet (events)                               =>', q(con, "SELECT COUNT(*) FROM events"))
        print('[SQL] Benchmark Matrix (benchmarks)               =>', q(con, "SELECT COUNT(*) FROM benchmarks"))
        print('[SQL] Devices                                     =>', q(con, "SELECT COUNT(*) FROM devices"))
        # Bonus: anomalies and event_log
        print('[SQL] Anomalies                                    =>', q(con, "SELECT COUNT(*) FROM anomalies"))
        print('[SQL] Event Log                                    =>', q(con, "SELECT COUNT(*) FROM event_log"))
        con.close()

    # Filesystem-backed tabs
    print('\n[FS] Log Viewer: logs/                            =>', exists("logs"))
    print('[FS] Triage Queue: logs/anomalies/                =>', exists("logs/anomalies"))
    print('[FS] Model Packs: models/packs/                   =>', exists("models/packs"))
    print('[FS] Pipelines: pipelines/                        =>', exists("pipelines"))
    print('[FS] Inspection Rules: config/inspection_rules.yaml =>', exists("config/inspection_rules.yaml"))
    print('[FS] Cameras: config/cameras.yaml                 =>', exists("config/cameras.yaml"))
    print('[FS] I/O Connectors: config/connectors/           =>', exists("config/connectors"))
    print('[FS] Governance: config/policy.yaml               =>', exists("config/policy.yaml"))
    print('[FS] Examples: examples/                          =>', exists("examples"))
    print('[FS] Benchmarks folder: benchmarks/               =>', exists("benchmarks"))
    print('[FS] XAI results: xai_results/                    =>', exists("xai_results"))
    print('[FS] MES Export CSV: mes_latest.csv               =>', exists("mes_latest.csv"))

    print("\nIf anything shows MISS or ERR, that's the reason a tab looks empty.")

if __name__ == "__main__":
    main()
