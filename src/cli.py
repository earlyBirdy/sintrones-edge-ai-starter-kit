#!/usr/bin/env python3
"""CLI Stub for Edge AI Starter Kit
Provides a single entrypoint that can call subcommands in this toolkit.
Extend with real commands as modules mature.
"""
import argparse, sys, importlib

def main():
    ap = argparse.ArgumentParser(prog="sintrones-edge-ai", description="Edge AI Starter Kit CLI (stub)")
    sub = ap.add_subparsers(dest="cmd")

    sub.add_parser("version", help="Print version")
    p_collect = sub.add_parser("collect", help="Run collector stub")
    p_collect.add_argument("--broker", default="localhost")
    p_collect.add_argument("--topic", default="factory/#")
    p_collect.add_argument("--out", default="data/collector/events.jsonl")

    p_batch = sub.add_parser("batch", help="Run batcher stub")
    p_batch.add_argument("--infile", default="data/collector/events.jsonl")
    p_batch.add_argument("--outdir", default="data/batches")

    args = ap.parse_args()
    if args.cmd == "version":
        print("sintrones-edge-ai CLI (stub) v0.0.0")
    elif args.cmd == "collect":
        mod = importlib.import_module("src.collector")
        sys.argv = ["collector.py", "--broker", args.broker, "--topic", args.topic, "--out", args.out]
        mod.main()
    elif args.cmd == "batch":
        mod = importlib.import_module("src.batcher")
        sys.argv = ["batcher.py", "--infile", args.infile, "--outdir", args.outdir]
        mod.main()
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
