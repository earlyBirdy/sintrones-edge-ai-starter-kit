#!/usr/bin/env python3
"""Collector Stub
Collects MQTT messages and writes them to local storage (JSONL/Parquet).
This is a minimal stub so the repo matches the README; extend as needed.
"""
import argparse, sys, json, time, pathlib

def main():
    ap = argparse.ArgumentParser(description="Collector (stub)")
    ap.add_argument("--broker", default="localhost", help="MQTT broker host")
    ap.add_argument("--topic", default="factory/#", help="MQTT topic")
    ap.add_argument("--out", default="data/collector/events.jsonl", help="Output JSONL file")
    args = ap.parse_args()

    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Stub: write a single example record and exit
    record = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "source": "collector-stub",
        "message": "hello from collector stub",
        "broker": args.broker,
        "topic": args.topic
    }
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    print(f"[collector] wrote sample record to {out}")

if __name__ == "__main__":
    main()
