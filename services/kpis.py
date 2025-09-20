from __future__ import annotations
from typing import Dict, Any, Optional, List
import sqlite3
from dataclasses import dataclass, asdict

from services.db import get_conn

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


def build_kpis() -> KpiReport:
    conn = get_conn()
    cur = conn.cursor()

    def _fetch_one(sql: str, params=()):
        cur.execute(sql, params)
        row = cur.fetchone()
        return row[0] if row else None

    total_devices = _fetch_one("SELECT COUNT(*) FROM devices") or 0
    active_devices_24h = _fetch_one("""
        SELECT COUNT(*) FROM devices
        WHERE last_seen_ts >= datetime('now', '-1 day')
    """) or 0
    total_readings = _fetch_one("SELECT COUNT(*) FROM sensor_readings") or 0
    total_inferences = _fetch_one("SELECT COUNT(*) FROM inference_events") or 0
    total_anomalies = _fetch_one("SELECT COUNT(*) FROM anomalies") or 0
    total_quality = _fetch_one("SELECT COUNT(*) FROM quality_results") or 0
    passed = _fetch_one("SELECT COUNT(*) FROM quality_results WHERE passed=1") or 0

    yield_rate = (passed / total_quality * 100.0) if total_quality else 0.0
    last_ingest_ts = _fetch_one("SELECT MAX(ts) FROM sensor_readings")

    cur.execute("SELECT device_id FROM devices ORDER BY device_id LIMIT 5")
    sample_devices = [r[0] for r in cur.fetchall()]

    conn.close()

    return KpiReport(
        total_devices=total_devices,
        active_devices_24h=active_devices_24h,
        total_readings=total_readings,
        total_inferences=total_inferences,
        total_anomalies=total_anomalies,
        total_quality_checks=total_quality,
        yield_rate_pct=round(yield_rate, 2),
        last_ingest_ts=last_ingest_ts,
        sample_devices=sample_devices,
    )
