#!/usr/bin/env python3
"""Release Agent
Runs tools/healthcheck.py and drafts dist/release_notes.md
"""
import argparse, json, subprocess, sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "dist"; DIST.mkdir(parents=True, exist_ok=True)

def run_healthcheck():
    script = ROOT / "tools" / "healthcheck.py"
    res = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    if res.returncode != 0:
        print("[release] healthcheck failed:", res.stderr)
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print("[release] invalid healthcheck JSON:", e)
        return None

def write_notes(tag, extra, report):
    ts = datetime.utcnow().strftime("%Y-%m-%d")
    lines = [f"# Release {tag} — {ts}\n"]
    if extra: lines += [extra, ""]
    if report:
        lines += ["## Readiness Summary", f"- Ready for run: **{report.get('ready_for_run')}**", ""]
        if report.get("syntax_errors"):
            lines.append("### Syntax Errors")
            for e in report["syntax_errors"][:20]:
                lines.append(f"- `{e['file']}` line {e['line']}: {e['msg']}")
            lines.append("")
        if report.get("missing_imports"):
            lines.append("### Missing Dependencies")
            for m in report["missing_imports"][:20]:
                lines.append(f"- `{m['package']}` (import `{m['import_name']}`): {m['error']}")
            lines.append("")
        lines.append("### Structure Checks")
        for k,v in (report.get("structure") or {}).items():
            lines.append(f"- {k}: {'OK' if v else 'MISSING'}")
        lines.append("")
        onnx = report.get("onnx") or {}
        lines.append("### ONNX")
        lines.append(f"- onnxruntime: {onnx.get('onnxruntime')}")
        lines.append(f"- model IR: {onnx.get('model_ir')} opsets: {onnx.get('opsets')}")
        if onnx.get("note"): lines.append(f"- note: {onnx['note']}")
        lines.append("")
    (DIST / "release_notes.md").write_text("\n".join(lines), encoding="utf-8")
    print("[release] wrote", (DIST/"release_notes.md").resolve())

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--notes", default="")
    args = ap.parse_args()
    rep = run_healthcheck()
    write_notes(args.tag, args.notes, rep)

if __name__ == "__main__":
    main()
