# Comparison for Edge AI Vision Inspection (Updated)

| Feature Category | Sintrones Edge AI Starter Kit | Cloud‑centric platform (typical) | Edge‑SDK toolkit (typical) | 💡 Implemented Enhancements |
|---|---|---|---|---|
| Edge‑First Architecture | ✅ Local runtime, file‑based packs, logs, offline‑friendly | ❌ Cloud‑first | ✅ Edge SDK, containers | **SQLite backbone**; hooks for edge‑to‑edge MQTT sync (gateway stub) |
| Model Packs & OTA | ✅ Versioned `modelpack.yaml`, validate/smoke, deploy/rollback | ⚠️ Cloud control plane | ✅ OTA / SDK available | **Staged & shadow deploy fields** in `deployments.policy` + event logs |
| Fleet Orchestration | ✅ Registry (devices, heartbeat, alarms) | ✅ Full cloud view | ✅ Device SDK + mgmt | **Fleet tab from SQLite**: uptime %, events, OTA history |
| Runtime Benchmarking | ✅ Sizes × ONNX/OpenVINO/TensorRT; auto‑select | ❌ Hidden | ✅ Perf surfaced | **Latency+accuracy gates** in `best_engine()` |
| Anomaly Detection | ✅ Review queue | ✅ Proprietary cloud | ✅ Defect‑ready | **Triage SLA/assignee** fields via events meta |
| Few‑Shot Training | 🧩 UI stub | ✅ Managed cloud | ⚠️ Off‑device | Hooks to export ONNX as a new Model Pack (doc) |
| Inference (Multi‑Mode) | 🔧 BYO runtime | ✅ Managed | ✅ SDK pipelines | Plugin API (`plugins/api.py`) for custom steps |
| Multi‑Camera & Sync | 🧩 Stubs | ✅ Production capture | ✅ Camera SDKs | Recipes placeholder; store per‑cam metrics in `sensor_readings` |
| Industrial I/O | 🧩 PASS/FAIL simulator | ✅ Connectors | ✅ Fieldbus stacks | MQTT schema + gateway path to MES (stub) |
| Data Traceability | ✅ Unified index | ✅ Deep record | ⚠️ Varies | **SQLite tables** `inspections/lineage`; image hashes planned |
| Triage Queue | ✅ Prioritized list | ✅ Curated | ✅ App‑dependent | **Reviewer SLAs, assignment** via events meta |
| Promote → Rules | ✅ YAML rules | ✅ Tests | ✅ Rules/graphs | **ROC assist** + A/B helper |
| Yield & Quality | ✅ Yield, DPPM, Pareto | ✅ Extensive BI | ⚠️ Basic→Adv | **SQL‑backed tab** with daily yield chart |
| Pipeline Builder | ✅ Exports YAML | ✅ Visual graphs | ✅ Graph/DSL | Version diff proposal + tests (docs) |
| Governance & Signing | ✅ SHA‑256 & lineage | ✅ Enterprise | ⚠️ Hooks | Lineage table + anchor_ref for optional anchoring |
| Cloud/Remote Sync | 🧩 MQTT WIP | ✅ Full | ✅ Optional | **Gateway sidecar stub** + CDC `changes` table |
| CI/CD & Release | ✅ Scriptable packs | ✅ Full pipelines | ✅ SDK flows | **GH Actions** workflow scaffold |
| Deployment Method | ✅ Python + Streamlit | ✅ SaaS | ✅ Containers | **Dockerfile/compose** for easy runs |
| Security & Residency | ✅ On‑device first | ⚠️ Tenancy | ⚠️ Options | RBAC note (todo), local users planned |
| Lock‑In / Extensibility | ✅ Open modules | ⚠️ Locked | ⚠️ SDK‑bounded | **Plugin API** for custom steps |
