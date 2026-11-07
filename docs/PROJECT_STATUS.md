# DFU-XAI Project Status & Milestone Ledger

**Project Title:** DFU-XAI: An Integrated Self-Supervised, Domain-Adaptive and Explainable AI Framework for Calibrated Longitudinal Diabetic Foot Ulcer Assessment and Monitoring  
**Current Phase:** Milestone 1 (COMPLETED) -> Transitioning to Milestone 2 & 3  
**Status Last Updated:** 2026-11-07  

---

## Milestone Progress Summary

| Milestone | Title | Status | Notes & Acceptance Criteria |
| :--- | :--- | :---: | :--- |
| **Milestone 0** | Repository & Environment Audit | **COMPLETED** | Hardware inspected (12 vCPUs, 15GB RAM, CPU-mode). Repository structure created. Docs initialized. |
| **Milestone 1** | Backend Foundation | **COMPLETED** | FastAPI app, SQLAlchemy models, Pydantic schemas, RBAC auth (`admin`, `clinician`, `researcher`, `viewer`), SQLite/Postgres dual-engine, 19/19 tests passing. |
| **Milestone 2** | Frontend Foundation | Pending | Next.js 14 App router, clinician dashboard, role-based shell, auth client. |
| **Milestone 3** | Data & Image Pipeline | **IN PROGRESS** | EXIF stripping, blur/exposure validation, circular/card scale calibration, procedural synthetic fixtures created. |
| **Milestone 4** | Segmentation Baseline | Pending | U-Net baseline, SegFormer-B0 candidate, Dice/IoU/HD95 metrics, overlay generator. |
| **Milestone 5** | SSL Comparison | Pending | DINOv2, SimCLR, MAE experiment harnesses, ImageNet baseline, patient-split manifests. |
| **Milestone 6** | Clinical & Longitudinal Analysis | Pending | Mixed-effects longitudinal rate modeling, clinical fusion (LightGBM/Logistic), visit progression timeline. |
| **Milestone 7** | XAI, Uncertainty & Domain Adaptation | Pending | Grad-CAM, SHAP feature attributions, MC Dropout/Ensemble uncertainty, domain shift test. |
| **Milestone 8** | Hybrid Deployment | Pending | PWA camera capture, ONNX export/runtime adapter, PDF clinical summary report. |
| **Milestone 9** | Final Validation & Handover | Pending | Automated test suite execution, threat audit, final implementation report. |

---

## Verified Component Status

- [x] Workspace & Hardware Audit (AMD Ryzen 5 5600H, CPU execution, no GPU)
- [x] Environment Check Script (`scripts/check_environment.py`)
- [x] Repository Skeleton & Directory Layout
- [x] Governance & Security Documentation (`docs/`)
- [x] Backend FastAPI App & Healthcheck (`backend/app/main.py`)
- [x] Database Relational Models (`backend/app/models/`)
- [x] JWT & Role-Based Access Control (`admin`, `clinician`, `researcher`, `viewer`)
- [x] Image Ingestion & EXIF Metadata Stripper (`backend/app/services/storage.py`)
- [x] Blur Score & Exposure Assessment (`backend/app/services/quality.py`)
- [x] Planar Scale Calibration & Metric Area Math (`backend/app/services/calibration.py`)
- [x] Longitudinal Trajectory & Progression Analyzer (`backend/app/services/longitudinal.py`)
- [x] De-identified Cohort CSV Export (`backend/app/api/v1/audit.py`)
- [x] Procedural Synthetic Wound Generator (`ml/preprocessing/synthetic.py`)
- [x] 19/19 Automated Pytest Suite Passing (`docs/TEST_REPORT.md`)
- [ ] Frontend App Router & Role Navigation (`frontend/`)
- [ ] PyTorch / ONNX ML Experiment Harnesses (`ml/models/`)

---

## Blocked & External Dependencies

1. **Approved Clinical Patient Datasets**: No real patient datasets or identifiable images are committed. Data loaders and manifests are implemented; training on institutional data is held pending formal institutional ethics review and data transfer agreements (DTA).
2. **GPU Acceleration**: Local host operates in CPU mode. ML modules use CPU-optimized tensor routines and ONNX/synthetic adapters for development.
