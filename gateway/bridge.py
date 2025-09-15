import json, paho.mqtt.client as mqtt
from core.db import connect
LOCAL_BROKER='localhost'; LOCAL_TOPIC='edge/+/inspection'

def send_to_cloud(payload: dict) -> str: return 'ack:ok'  # TODO

def on_message(client, userdata, msg):
    con = userdata['con']; payload = json.loads(msg.payload.decode()); ack = send_to_cloud(payload)
    con.execute("""INSERT INTO events(ts, device_id, severity, type, message, meta_json)
                 VALUES (datetime('now'), ?, 'info', 'forward', ?, json(?))""",
                (payload.get('device_id','local'), 'inspection_forward', json.dumps({'ack': ack})))

def run():
    con = connect(); cli = mqtt.Client(userdata={'con': con}); cli.on_message = on_message
    cli.connect(LOCAL_BROKER,1883,60); cli.subscribe(LOCAL_TOPIC,1); cli.loop_forever()

if __name__=='__main__': run()
