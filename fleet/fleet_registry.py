import os, json, time
REG_PATH="fleet/devices.json"
def _load():
    if os.path.exists(REG_PATH): return json.load(open(REG_PATH))
    return {"devices":[{"id":"edge-01","hw":"x86_64","accel":"cpu","pack":"-","last_heartbeat":None,"alarms":[]} ]}
def _save(d): os.makedirs(os.path.dirname(REG_PATH), exist_ok=True); json.dump(d, open(REG_PATH,"w"), indent=2)
def list_devices(): return _load()["devices"]
def heartbeat(device_id):
    d=_load()
    for dev in d["devices"]:
        if dev["id"]==device_id: dev["last_heartbeat"]=time.strftime("%Y-%m-%dT%H:%M:%S")
    _save(d)
def set_active_pack(device_id, pack):
    d=_load()
    for dev in d["devices"]:
        if dev["id"]==device_id: dev["pack"]=pack
    _save(d)
def raise_alarm(device_id, msg):
    d=_load()
    for dev in d["devices"]:
        if dev["id"]==device_id: dev.setdefault("alarms",[]).append({"ts":time.time(),"message":msg})
    _save(d)
