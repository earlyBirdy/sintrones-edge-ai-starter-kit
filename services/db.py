from __future__ import annotations
import os
import sqlite3
from pathlib import Path
from typing import Iterable, Tuple, Any, List, Dict

DB_PATH = str(Path(os.getenv("EDGEKIT_DB_PATH", "data/edgekit.db")).resolve())

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def q_one(sql: str, params: Tuple[Any, ...] = ()) -> Any:
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        row = cur.fetchone()
        return None if row is None else (row[0] if len(row.keys()) == 1 else dict(row))

def q_all(sql: str, params: Tuple[Any, ...] = ()) -> List[Dict[str, Any]]:
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return [dict(r) for r in cur.fetchall()]

def q_iter(sql: str, params: Tuple[Any, ...] = ()) -> Iterable[sqlite3.Row]:
    conn = get_conn()
    try:
        for row in conn.execute(sql, params):
            yield row
    finally:
        conn.close()
