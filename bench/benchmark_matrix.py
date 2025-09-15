from core.db import connect, migrate
def record_benchmark(device_id, engine, input_hw, input_size, fps, latency_ms, accuracy, notes=""):
    con = connect(); migrate(con)
    con.execute("INSERT INTO benchmarks(ts, device_id, engine, input_hw, input_size, fps, latency_ms, accuracy, notes) VALUES (datetime('now'),?,?,?,?,?,?,?,?)",(device_id, engine, input_hw, input_size, fps, latency_ms, accuracy, notes))
def best_engine(device_id, min_accuracy=0.0, max_latency_ms=1e9):
    con = connect()
    rows = con.execute("""SELECT engine, input_size, AVG(latency_ms) AS lat, AVG(accuracy) AS acc, AVG(fps) AS fps
                          FROM benchmarks WHERE device_id=? GROUP BY engine, input_size
                          HAVING acc >= ? AND lat <= ? ORDER BY lat ASC, acc DESC LIMIT 1""",(device_id, min_accuracy, max_latency_ms)).fetchone()
    return dict(rows) if rows else None
