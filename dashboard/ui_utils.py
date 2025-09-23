from __future__ import annotations
import os, sqlite3
from pathlib import Path

DB_PATH = Path(os.getenv("EDGE_DB_PATH") or (Path.cwd() / "data" / "edgekit.db"))

def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def table_exists(con, name: str) -> bool:
    try:
        cur = con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view') AND name=?;", (name,))
        return cur.fetchone() is not None
    except Exception:
        return False
