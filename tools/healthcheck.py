#!/usr/bin/env python3
"""
Edge AI Starter Kit — Repo Healthcheck
- Syntax check of all .py files
- Dependency import check from requirements.txt
- Structure checks for key files
- Optional: ONNX model IR vs onnxruntime support

Run:
  python tools/healthcheck.py
"""
from pathlib import Path
import sys, re, json

ROOT = Path(__file__).resolve().parents[1] if (Path(__file__).parent.name == "tools") else Path.cwd()

def gather_files():
    py_files = sorted([p for p in ROOT.rglob("*.py") if ".venv" not in p.parts and "site-packages" not in p.parts])
    req = next((p for p in ROOT.rglob("requirements.txt")), None)
    readmes = sorted([p for p in ROOT.rglob("README*.md")])
    return py_files, req, readmes

def syntax_check(py_files):
    errors = []
    for f in py_files:
        try:
            src = f.read_text(encoding="utf-8", errors="ignore")
            compile(src, str(f), "exec")
        except SyntaxError as e:
            errors.append({
                "file": str(f.relative_to(ROOT)),
                "line": e.lineno, "offset": e.offset,
                "text": e.text.strip() if e.text else "",
                "msg": e.msg
            })
        except Exception:
            # non-syntax exception on compile is ignored for static check
            pass
    return errors

def read_requirements(req_path):
    if not req_path or not req_path.exists(): return []
    pkgs = []
    for line in req_path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"): continue
        pkgs.append(s)
    return pkgs

def try_imports(pkgs):
    missing = []
    mapping = {
        "opencv-python": "cv2",
        "paho-mqtt": "paho.mqtt.client",
        "pyyaml": "yaml",
        "pyarrow": "pyarrow",
        "onnxruntime": "onnxruntime",
        "onnxruntime-gpu": "onnxruntime",
        "opcua": "opcua",
        "requests": "requests",
        "streamlit": "streamlit",
        "fastapi": "fastapi",
    }
    for pkg in pkgs:
        base = re.split(r"[<>=\[]", pkg, 1)[0].strip()
        modname = mapping.get(base, base)
        try:
            __import__(modname)
        except Exception as e:
            missing.append({"package": pkg, "import_name": modname, "error": str(e).split("\n")[0]})
    return missing

def structure_checks():
    checks = {
        "examples/vision_inspection/camera_infer.py": (ROOT / "examples" / "vision_inspection" / "camera_infer.py").exists(),
        "models/defect_detector.onnx": (ROOT / "models" / "defect_detector.onnx").exists(),
        "src/decision_engine/engine.py": (ROOT / "src" / "decision_engine" / "engine.py").exists(),
        "src/decision_engine/policies.yaml": (ROOT / "src" / "decision_engine" / "policies.yaml").exists(),
        "configs/config.yaml": (ROOT / "configs" / "config.yaml").exists(),
        "src/cli.py": (ROOT / "src" / "cli.py").exists(),
        "src/collector.py": (ROOT / "src" / "collector.py").exists(),
        "src/batcher.py": (ROOT / "src" / "batcher.py").exists(),
    }
    return checks

def onnx_check():
    info = {"onnxruntime": None, "model_ir": None, "opsets": None, "warning": None}
    model = ROOT / "models" / "defect_detector.onnx"
    try:
        import onnx
        if model.exists():
            m = onnx.load(str(model))
            info["model_ir"] = int(getattr(m, "ir_version", 0))
            info["opsets"] = [(imp.domain or "", int(imp.version)) for imp in m.opset_import]
    except Exception as e:
        info["warning"] = f"ONNX not importable or model unreadable: {e}"
    try:
        import onnxruntime as ort
        info["onnxruntime"] = ort.__version__
        # Simple heuristic on IR support: newer ORT supports newer IR;
        # users often hit IR11 vs max IR10 — emit guidance if model_ir and ORT mismatch
        if info["model_ir"] is not None and info["model_ir"] >= 11:
            pass
    except Exception as e:
        info["warning"] = f"onnxruntime not importable: {e}"
    return info

def main():
    py_files, req, readmes = gather_files()
    syntax = syntax_check(py_files)
    reqs = read_requirements(req)
    missing = try_imports(reqs)
    structure = structure_checks()
    onnxinfo = onnx_check()

    # High-level readiness
    ready = True
    if syntax or missing or not all(structure.values()):
        ready = False

    report = {
        "repo_root": str(ROOT),
        "py_files": len(py_files),
        "readmes_found": [str(p.relative_to(ROOT)) for p in readmes],
        "requirements_file": str(req.relative_to(ROOT)) if req else None,
        "structure": structure,
        "syntax_errors": syntax,
        "requirements_list": reqs,
        "missing_imports": missing,
        "onnx_info": onnxinfo,
        "ready_for_run": ready
    }
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
