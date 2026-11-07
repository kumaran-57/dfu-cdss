# DFU-XAI: Research Decision-Support Prototype

> **CLINICAL NOTICE:**  
> This software is an academic decision-support research prototype designed for clinician supervision. It is **not** certified as a medical device. It does **not** autonomously diagnose diabetic foot ulcers, prescribe treatment plans, or replace clinical judgment. All clinical decisions must be made by qualified healthcare professionals.

---

## Overview

**DFU-XAI** is an integrated software platform and experimental framework for calibrated, longitudinal diabetic foot ulcer assessment. The platform combines:

1. **Standardized Capture & Image Quality Control**: Smartphone camera capture with automated blur, exposure, and framing checks.
2. **Geometric Calibration**: Millimeter-scale and color reference detection for true metric area ($cm^2$) and Feret diameter measurement.
3. **Deep Segmentation**: Comparative evaluation of U-Net and SegFormer-B0 backbones for wound boundary and tissue classification.
4. **Self-Supervised Learning (SSL) Harness**: Controlled benchmark comparing ImageNet-pretrained representations against DINOv2, SimCLR, and MAE.
5. **Multimodal Clinical Fusion**: Fusion of image-derived wound metrics with tabular clinical biomarkers (HbA1c, neuropathy, vascular ABI).
6. **Longitudinal Trajectory Modeling**: Multi-visit wound healing tracking and mixed-effects regression rate estimation.
7. **Explainability & Calibrated Uncertainty**: Grad-CAM, SHAP feature attributions, and Monte Carlo Dropout epistemic uncertainty with automated clinician-review abstention.

---

## System Architecture

The prototype is organized into a modular full-stack architecture:
- `backend/`: Python FastAPI REST application with Pydantic V2, SQLAlchemy 2.0, and JWT RBAC authentication.
- `frontend/`: Next.js 14 App Router, TypeScript, and responsive Tailwind UI.
- `ml/`: Modular ML pipelines for image calibration, segmentation, SSL experiment adapters, and uncertainty quantification.
- `experiments/`: Experiment configurations (E1–E10), execution scripts, and reporting logs.
- `docs/`: Comprehensive system documentation, ethics checklists, threat models, and architectural decisions.

---

## Quickstart Guide

### 1. Environment Verification
```bash
python3 scripts/check_environment.py
```

### 2. Backend Setup & Local Server
```bash
# Configure environment (defaults to SQLite for local development)
cp .env.example .env

# Run automated tests
pytest backend/tests ml/tests -v

# Start FastAPI development server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```
Interactive API documentation will be available at: `http://localhost:8000/docs`.

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## Documentation Links
- [System Architecture & ER Diagram](docs/SYSTEM_ARCHITECTURE.md)
- [Data Dictionary](docs/DATA_DICTIONARY.md)
- [Data Governance & Ethics](docs/DATA_GOVERNANCE.md)
- [Threat Model](docs/THREAT_MODEL.md)
- [API Reference Guide](docs/API_GUIDE.md)
- [Experiment Plan (E1–E10)](docs/EXPERIMENT_PLAN.md)
- [Architectural Decisions (ADRs)](docs/DECISIONS.md)
- [Known Limitations](docs/KNOWN_LIMITATIONS.md)
- [Project Status Ledger](docs/PROJECT_STATUS.md)
