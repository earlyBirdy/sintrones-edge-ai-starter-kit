#!/usr/bin/env python3
"""Adapter Auto-Generation Agent
- MQTT sniff mode: listens to a wildcard topic for N samples and infers fields
- OPC UA browse mode: enumerates nodeIds and proposes a basic mapping

Writes proposed YAML to dist/config.autogen.yaml and prints to stdout.
"""
import argparse, time, json, re
from pathlib import Path
import yaml

def propose_from_mqtt(host, port, topic, samples=20, timeout=15):
    import paho.mqtt.client as mqtt
    fields=set(); messages=[]

    def on_connect(c,u,f,rc,prop=None):
        c.subscribe(topic); print("[autogen] subscribed:", topic)
    def on_message(c,u,msg):
        try:
            payload=json.loads(msg.payload.decode("utf-8"))
            messages.append(payload)
            for k in payload.keys(): fields.add(k)
        except Exception: pass

    cli=mqtt.Client(); cli.on_connect=on_connect; cli.on_message=on_message
    cli.connect(host, port, 60); cli.loop_start()
    t0=time.time()
    try:
        while len(messages) < samples and time.time()-t0 < timeout:
            time.sleep(0.2)
    finally:
        cli.loop_stop()

    cfg={
        "sources":{
            "mqtt_autogen":{
                "enabled":True,
                "host":host,"port":port,"topic":topic,
                "mappings":{
                    "temperature":"temperature" if "temperature" in fields else "your_temp_field",
                    "vibration":"vibration" if "vibration" in fields else "your_vib_field"
                }
            }
        }
    }
    return cfg, messages[:5]

def propose_from_opcua(endpoint, max_nodes=10):
    try:
        from opcua import Client
    except Exception as e:
        raise SystemExit("opcua not installed. pip install opcua") from e

    c=Client(endpoint); c.connect()
    nodes=[]
    try:
        obj=c.get_objects_node()
        for ch in obj.get_children()[:max_nodes]:
            try:
                nid=ch.nodeid.to_string()
                name=ch.get_browse_name().Name
                nodes.append({"nodeId":nid,"name":name})
            except Exception: pass
    finally:
        c.disconnect()

    cfg={
        "sources":{
            "opcua_autogen":{
                "enabled":True,
                "endpoint":endpoint,"source":"opcua-autogen",
                "nodes":[{"nodeId":n["nodeId"],"field":"temperature" if re.search("temp", n["name"], re.I) else ""} for n in nodes]
            }
        }
    }
    return cfg, nodes

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["mqtt","opcua"], required=True)
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--port", type=int, default=1883)
    ap.add_argument("--topic", default="factory/#")
    ap.add_argument("--samples", type=int, default=20)
    ap.add_argument("--timeout", type=int, default=15)
    ap.add_argument("--endpoint")
    ap.add_argument("--out", default="dist/config.autogen.yaml")
    args=ap.parse_args()

    Path("dist").mkdir(parents=True, exist_ok=True)
    if args.mode=="mqtt":
        cfg, sample=propose_from_mqtt(args.host,args.port,args.topic,args.samples,args.timeout)
    else:
        if not args.endpoint: raise SystemExit("--endpoint required for OPC UA mode")
        cfg, sample=propose_from_opcua(args.endpoint)

    with open(args.out,"w") as f: yaml.safe_dump(cfg,f,sort_keys=False)
    print("# --- Proposed Adapter Config ---")
    print(yaml.safe_dump(cfg, sort_keys=False))
    print("# --- Sample ---")
    print(json.dumps(sample, indent=2))

if __name__=="__main__":
    main()
