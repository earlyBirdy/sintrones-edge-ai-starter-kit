# Sintrones Edge AI Vision Inspection — Software Integration Proposal

**Client:** The Buyers (Factory QA / IIoT)  
**Vendor:** Sintrones  
**Date:** 2025-09-15

---

## 1) Executive Summary
Sintrones proposes a staged software integration of the **Edge AI Starter Kit** to deliver deterministic vision inspection at the edge, with **unit‑level traceability**, **yield dashboards**, **model lifecycle (Model Packs)**, and **fleet orchestration**. The solution is **local‑first**, runs offline, and integrates with PLC/MES via **MQTT/OPC‑UA/Modbus**.

**Outcomes**
- Faster time‑to‑demo and pilot on real stations (days → weeks).  
- Deterministic **PASS/FAIL** to PLC with audited rules and lineage.  
- Lower TCO vs. cloud‑centric platforms; no lock‑in, open formats (ONNX/SQLite/CSV).

---

## 2) Scope of Work
**In scope**
- Streamlit dashboard (17 tabs) deployment and configuration
- On‑device **SQLite** for inspections/devices/deployments/benchmarks/events/lineage
- **Model Packs**: package, validate/smoke, staged/shadow/rollback deployments
- **Benchmark Matrix**: auto-select ONNX/OpenVINO/TensorRT by **latency & accuracy**
- **Traceability & Yield** (SQL tabs): unit logs, DPPM, Pareto, trends
- **Triage → Rule** workflow: ROC/A‑B helpers for pass/fail thresholds
- Connectors: PLC triggers (OPC‑UA/Modbus), **MQTT** events to MES (topic schema agreed)

**Out of scope (available as add‑ons)**
- Custom model training at scale; private cloud dashboards; SSO/RBAC; DVC/Git‑LFS dataops; hard real‑time I/O; turnkey lighting/optics; extended change‑control documentation.

---

## 3) Stages, Timeline & Deliverables

| Stage | Duration | Key Activities | Deliverables |
|---|---:|---|---|
| 0. Discovery & Planning | 5–7 days | Requirements, stations, cameras, PLC/MES interfaces, acceptance criteria | Project plan, interface spec, success metrics |
| 1. Environment & Baseline | 5–7 days | Install repo, create venv/containers, **init SQLite**, seed sample data, connect cameras | Running dashboard, baseline capture/logging |
| 2. Pipeline & Model Pack | 5–7 days | Define `recipes/pipeline.yaml`, wrap model as **Model Pack**, smoke tests | Model Pack v1, smoke‑test report |
| 3. Benchmark & Runtime | 5–7 days | **Benchmark Matrix** gating (accuracy+latency), pick runtime/size | Benchmark report, selected runtime profile |
| 4. Line Integration | 5–7 days | PLC I/O mapping (OPC‑UA/Modbus), **MQTT** to MES, PASS/FAIL wiring | Live station with deterministic intercepts |
| 5. Triage → Rule Tuning | 5–7 days | Label & ROC/A‑B, thresholds, rule promotion, A/B on live feed | Rule set v1, configuration bundle |
| 6. Pilot (5–20 units) | 3–5 weeks | Staged/shadow deployments, operator feedback, yield tracking | Pilot report: Yield, DPPM, Pareto, lessons |
| 7. Prod Hardening & Handover | 3–5 weeks | Fleet alarms, rollback drills, runbooks, training | Handover pack, rollback SOP, admin training |

> **Typical elapsed:** PoC ~ **2 weeks**; Pilot **4–6 weeks**; Production **6–10 weeks** after pilot.

---

## 4) Pricing Model (pegged to compute unit cost **C** per station)

**Up‑front software + integration (per station)**
- **PoC (1–3 units):** **0.9×–1.5× C**  
- **Pilot (5–20 units):** **1.5×–2.5× C**  
- **Production (20+ units):** **3.5×–5.0× C** (includes fleet/rollback/ops)

**Annual software care & updates:** **15–25%** of up‑front software fee  

**Adders (if applicable)**
- Per extra camera on a station: **+0.5×–1.5× C**  
- Custom model fine‑tuning per iteration: **0.5×–1× C**  
- Enterprise features (SSO/RBAC, change‑control docs, hard real‑time I/O): **+0.5×–0.9× C**  
- Hardware pass‑through margin (if supplied by Sintrones): **+10–15%**

**Quick example**
- If **C = $3,000**:  
  - Pilot per station ≈ **$4,500–$7,500** up‑front, remote support ≈ **$900–$1,875/yr** (at 20–25%).

---

## 5) Commercial Terms
- **Payment milestones**: 40% (kickoff) / 40% (pilot go‑live) / 20% (handover)  
- **Validity**: 60 days from issue  
- **Travel & expenses**: actuals at cost (pre‑approved)  
- **Hardware**: quoted separately (if required)

---

## 6) Acceptance Criteria
- Deterministic **PASS/FAIL** signals to PLC within target latency (e.g., ≤200 ms camera‑to‑decision on target hardware/rule).  
- **Yield dashboard** shows real data (PASS/FAIL, DPPM, Pareto) for pilot units.  
- **Traceability** records include: serial, station, shift, vendor, model@ver, rule@ver, result, score, timestamp, and image pointer.  
- **Model Pack**: validated v1 with benchmark record; rollback drill executed.  

---

## 7) Assumptions & Dependencies
- Customer provides: compute unit spec, camera model(s), optics/lighting, sample units, PLC/MES endpoints, line time for integration.  
- Data residency: images retained on device; CSV/Parquet export allowed for BI unless otherwise specified.  
- Network: LAN access for PLC/MES; internet not required at runtime.  
- Security: local admin access for install and service accounts for MES/MQTT/OPC‑UA where applicable.

---

## 8) RACI (summary)
- **Sintrones**: Dashboard & DB setup, Model Pack packaging, Benchmark Matrix, rules tuning (ROC/A‑B), fleet staging/rollback, runbooks.  
- **Customer**: Camera/lighting, PLC mapping & signals, MES endpoints, acceptance testing, operators’ feedback.  
- **Joint**: Data labeling for triage, performance targets, SOP approval.

---

## 9) Risks & Mitigations
- **Lighting/optics variability** → conduct quick DOEs; lock exposure/lighting SOP.  
- **Latency sensitivity** → benchmark early; select TensorRT/OpenVINO where needed.  
- **Label drift** → triage cadence; periodic threshold audits with ROC/A‑B.  
- **Change control** → Model Packs with signatures and rollbacks; SOPs for deploy.

---

## 10) Next Steps
1. Confirm scope, stations, and compute unit **C**.  
2. Kickoff workshop (Stage 0).  
3. Issue PO & schedule Stage 1 start date.  

**Contact:** birdycho@sintrones.com | https://www.sintrones.com/contact/
