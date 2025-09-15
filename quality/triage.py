from core.db import connect, migrate
def add_triage_item(unit_id, score, defect_label, assignee=None, sla_hours=24, note=""):
    con = connect(); migrate(con)
    con.execute("""INSERT INTO events(ts, device_id, severity, type, message, meta_json)
                   VALUES (datetime('now'), 'local', 'info', 'triage_add', ?, json(?))""",
                (f"unit:{unit_id}", f'{{"score":{score},"label":"{defect_label}","assignee":"{assignee}","sla_h":{sla_hours},"note":"{note}"}}'))