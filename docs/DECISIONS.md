# Architectural Decision Records (ADRs)

## ADR-001: Local Environment and Hardware Strategy
* **Date:** 2026-11-07
* **Status:** Accepted
* **Context:** The development host is a 12-thread AMD Ryzen 5 5600H CPU system with 15 GiB RAM and no discrete NVIDIA GPU.
* **Decision:** All machine learning inference and image processing pipelines will natively support CPU execution. Heavyweight model dependencies (PyTorch, ONNX Runtime) will be wrapped in modular adapter classes with graceful synthetic/mock fallbacks so that the complete API, web UI, calibration math, and longitudinal dashboards are fully verifiable and testable without requiring GPU hardware.
* **Consequences:** Ensures 100% testability on developer workstations and lightweight edge devices. Full model retraining on massive datasets must be orchestrated on approved GPU compute clusters.

---

## ADR-002: Dual-Engine Database Architecture (SQLite & PostgreSQL)
* **Date:** 2026-11-07
* **Status:** Accepted
* **Context:** The system needs zero-dependency local execution for testing and CI while maintaining enterprise hospital deployment readiness.
* **Decision:** Use SQLAlchemy 2.0 with standard declarative models and abstract session management. Default to SQLite (`sqlite:///./dfu_xai.db`) for immediate out-of-the-box local operation, while allowing instant drop-in PostgreSQL support by configuring the standard `DATABASE_URL` environment variable.
* **Consequences:** Developers and automated CI test suites can execute without needing external Postgres daemons, while production setups can use PostgreSQL with full JSONB and concurrent transaction support.

---

## ADR-003: Privacy & Ethics-First Data Ingestion
* **Date:** 2026-11-07
* **Status:** Accepted
* **Context:** Real DFU patient data contains protected health information (PHI) and biometric identifiers.
* **Decision:**
  1. No real patient data will ever be committed to the repository or transmitted to unapproved third-party cloud services.
  2. All participant records use non-identifying coded study IDs (e.g., `PART-001`).
  3. Image ingestion automatically strips all EXIF and hardware metadata.
  4. Demo mode and automated unit tests operate strictly on procedurally generated synthetic fixtures marked with `is_synthetic = True`.
* **Consequences:** Prevents inadvertent privacy breaches and complies with medical research ethics standards.

---

## ADR-004: Modular Machine Learning & Experiment Harness
* **Date:** 2026-11-07
* **Status:** Accepted
* **Context:** The master specification requires evaluating 4 representation methods (ImageNet, DINOv2, SimCLR, MAE), 2 segmentation backbones (U-Net, SegFormer-B0), domain adaptation, and clinical fusion across experiments E1–E10.
* **Decision:** Implement abstract base classes (`BaseSegmentationModel`, `BaseEncoder`, `BaseFusionModel`) with unified signatures for inference, feature extraction, and uncertainty estimation. All experiment runs are strictly driven by versioned configuration files (`experiments/configs/*.yaml`) with patient-level split validation.
* **Consequences:** Decouples the API server from specific model weights and guarantees scientific reproducibility across experimental runs.
