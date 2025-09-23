#!/usr/bin/env python3
"""Repo wiring scanner
Run from your repo root:
  python scan_dispatch_map.py

What it does:
- Scans all *.py files for:
  - DISPATCH blocks and entries
  - TAB_TITLES blocks
  - lines containing 'dispatch', 'mapped to', 'map to', 'router', 'route', 'tabs'
- Flags DISPATCH entries that use 'lambda'
- Inventories all functions named like 'render_*' with their module path
- Prints a concise report with file:line references

Tips:
- Add '--json' to print machine-readable JSON of findings as well.
- Add '--only python|--only app' to restrict (optional; defaults to all .py).
"""
from __future__ import annotations
import re, sys, json
from pathlib import Path
from typing import Dict, List, Any, Tuple

ROOT = Path.cwd()

KEYWORDS = [
    r"\bDISPATCH\b",
    r"\bTAB_TITLES\b",
    r"\bmapped\s+to\b",
    r"\bmap\s+to\b",
    r"\bdispatch\b",
    r"\brouter\b",
    r"\broute\b",
    r"\btabs\b",
]

RENDER_DEF_RX = re.compile(r"^\s*def\s+(render_[A-Za-z0-9_]+)\s*\(\)", re.M)
DISPATCH_BLOCK_RX = re.compile(r"DISPATCH\s*=\s*\{(.*?)\}", re.S)
TAB_TITLES_RX = re.compile(r"TAB_TITLES\s*=\s*\[(.*?)\]", re.S)
DISPATCH_PAIR_RX = re.compile(r"['\"](.*?)['\"]\s*:\s*([A-Za-z0-9_\.]+)")

def read(p: Path) -> str:
    return p.read_text(encoding='utf-8', errors='ignore')

def scan_file(p: Path) -> Dict[str, Any]:
    txt = read(p)
    findings: Dict[str, Any] = {"path": str(p), "dispatch": [], "tab_titles": [], "keywords": [], "renders": []}

    # DISPATCH entries
    for m in DISPATCH_BLOCK_RX.finditer(txt):
        block = m.group(1)
        entries = DISPATCH_PAIR_RX.findall(block)
        findings["dispatch"].append({"entries": entries, "span": m.span()})
    # TAB_TITLES
    for m in TAB_TITLES_RX.finditer(txt):
        block = m.group(1)
        titles = re.findall(r"['\"](.*?)['\"]", block)
        findings["tab_titles"].append({"titles": titles, "span": m.span()})
    # RENDER defs
    defs = RENDER_DEF_RX.findall(txt)
    if defs:
        findings["renders"] = defs
    # keyword lines
    lines = txt.splitlines()
    for i, line in enumerate(lines, 1):
        for kw in KEYWORDS:
            if re.search(kw, line, re.I):
                findings["keywords"].append({"line": i, "text": line.strip()[:240]})
                break
    return findings

def walk_files(only: str | None = None) -> List[Path]:
    files = []
    for p in ROOT.rglob("*.py"):
        if "venv" in p.parts or ".venv" in p.parts or "__pycache__" in p.parts:
            continue
        if only == "app" and p.name != "app.py":
            continue
        files.append(p)
    return files

def main():
    only = None
    out_json = False
    for a in sys.argv[1:]:
        if a == "--json": out_json = True
        elif a.startswith("--only"): only = a.split(" ")[-1] if " " in a else None

    files = walk_files(only)
    all_findings = [scan_file(p) for p in files]
    # Aggregate
    dispatch_files = [f for f in all_findings if f["dispatch"]]
    tabs_files = [f for f in all_findings if f["tab_titles"]]
    lambdas: List[Tuple[str,str]] = []
    render_index: Dict[str,List[str]] = {}

    for f in all_findings:
        for d in f["dispatch"]:
            for k,v in d["entries"]:
                if v.strip() == "lambda":
                    lambdas.append((f["path"], k))
        for r in f.get("renders", []):
            render_index.setdefault(r, []).append(f["path"])

    # Report
    print("== Files with DISPATCH ==")
    for f in dispatch_files:
        print("-", f["path"])
        for d in f["dispatch"]:
            pairs = d["entries"]
            if not pairs:
                print("   (no entries parsed)")
                continue
            for k,v in pairs:
                print(f"   {k} -> {v}")

    print("\n== Files with TAB_TITLES ==")
    for f in tabs_files:
        print("-", f["path"])
        for t in f["tab_titles"]:
            titles = t["titles"]
            print("   ", titles)

    if lambdas:
        print("\n[FAIL] 'lambda' found in DISPATCH entries (these tabs will look identical):")
        for path, key in lambdas:
            print(f"  {path}: {key}")

    print("\n== render_* function definitions (by name) ==")
    for name, paths in sorted(render_index.items()):
        print(f"  {name}: ")
        for p in paths:
            print(f"    - {p}")

    # keyword hits
    print("\n== keyword hits (dispatch/map/router/tabs) ==")
    for f in all_findings:
        hits = f["keywords"]
        if not hits: continue
        print("-", f["path"])
        for h in hits[:10]:  # show top 10 per file
            print(f"   L{h['line']:>4}: {h['text']}")
        if len(hits) > 10:
            print(f"   ... +{len(hits)-10} more lines ...")


    if out_json:
        print("\n=== JSON ===")
        print(json.dumps(all_findings, indent=2))

if __name__ == "__main__":
    main()
