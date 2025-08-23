#!/usr/bin/env python3
"""System Recovery Agent
- Subscribes to MQTT heartbeat topics (e.g., factory/health/#)
- If no heartbeat is received for `timeout_sec`, executes a recovery action

Usage:
  python -m src.agents.system_recovery_agent --config agents/system_recovery.yaml
"""
import argparse, time, json, subprocess
from datetime import datetime, timezone
from collections import defaultdict
import yaml
import paho.mqtt.client as mqtt

def _now():
    return datetime.now(timezone.utc).timestamp()

def run(cfg_path: str):
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f) or {}

    m = cfg.get("mqtt", {})
    r = cfg.get("recovery", {})
    topic   = m.get("topic", "factory/health/#")
    host    = m.get("host", "localhost")
    port    = int(m.get("port", 1883))
    timeout = int(r.get("timeout_sec", 30))
    actions = r.get("actions", {})

    last_seen = defaultdict(lambda: 0.0)

    def on_connect(cli, u, flags, rc, p=None):
        print("[recovery] connected rc=", rc)
        cli.subscribe(topic); print("[recovery] subscribed:", topic)

    def on_message(cli, u, msg):
        src = msg.topic.split("/")[-1]
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            src = payload.get("source", src)
        except Exception:
            pass
        last_seen[src] = _now()
        print(f"[recovery] heartbeat: {src}")

    cli = mqtt.Client()
    cli.on_connect = on_connect
    cli.on_message = on_message
    cli.connect(host, port, 60)
    cli.loop_start()

    try:
        while True:
            now = _now()
            for src, ts in list(last_seen.items()):
                if now - ts > timeout:
                    print(f"[recovery] TIMEOUT {src} ({int(now-ts)}s). Executing recovery.")
                    action = actions.get(src) or actions.get("default") or {}
                    shell = action.get("shell")
                    if shell:
                        try:
                            subprocess.run(shell, shell=True, check=False)
                            print("[recovery] ran:", shell)
                        except Exception as e:
                            print("[recovery] ERROR running action:", e)
                    last_seen[src] = now
            time.sleep(2)
    except KeyboardInterrupt:
        pass
    finally:
        cli.loop_stop()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="agents/system_recovery.yaml")
    args = ap.parse_args()
    run(args.config)
