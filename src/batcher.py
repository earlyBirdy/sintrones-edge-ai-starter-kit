#!/usr/bin/env python3
"""Batcher Stub
Reads JSONL events and rolls them into time-partitioned files.
This is a minimal stub for structure alignment.
"""
import argparse, sys, pathlib, shutil, time

def main():
    ap = argparse.ArgumentParser(description="Batcher (stub)")
    ap.add_argument("--infile", default="data/collector/events.jsonl", help="Input JSONL file")
    ap.add_argument("--outdir", default="data/batches", help="Output directory")
    args = ap.parse_args()

    infile = pathlib.Path(args.infile)
    outdir = pathlib.Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    if not infile.exists():
        print(f"[batcher] input not found: {infile}")
        return
    ts = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    outfile = outdir / f"batch_{ts}.jsonl"
    shutil.copyfile(infile, outfile)
    print(f"[batcher] rolled {infile} -> {outfile}")

if __name__ == "__main__":
    main()
