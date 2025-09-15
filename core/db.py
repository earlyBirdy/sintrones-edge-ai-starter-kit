from pathlib import Path
import sqlite3, json
SCHEMA_FILE = Path(__file__).with_name("schema.sql")
DB_PATH = Path("data/edge.db")
def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH, check_same_thread=False, isolation_level=None)
    con.execute("PRAGMA journal_mode=WAL;")
    con.execute("PRAGMA synchronous=NORMAL;")
    con.execute("PRAGMA foreign_keys=ON;")
    con.row_factory = sqlite3.Row
    return con
def migrate(con=None):
    close_after = False
    if con is None:
        con = connect(); close_after = True
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        con.executescript(f.read())
    if close_after: con.close()
def dicts(rows): return [dict(r) for r in rows]
def insert_change(con, table, op, pk, row):
    con.execute("INSERT INTO changes(table_name, op, pk, row_json) VALUES (?,?,?,?)",(table,op,pk,json.dumps(row)))