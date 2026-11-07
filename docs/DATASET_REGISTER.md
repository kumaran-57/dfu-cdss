# DFU-XAI Dataset Register

This register catalogs public benchmarks and institutional datasets utilized or evaluated for the DFU-XAI project, detailing licenses and access status.

---

## Registered Datasets

### 1. DFUC2020 (Diabetic Foot Ulcer Challenge 2020)
- **Modality**: RGB Clinical Photography (Patch detection / Localization)
- **Origin**: Lancashire Teaching Hospitals NHS Trust & Manchester Metropolitan University
- **License**: Research-use only via MICCAI / End-User License Agreement
- **Status in Prototype**: Format adapter implemented (`ml/data/loaders/dfuc2020.py`). Raw data not committed to Git.

### 2. DFUC2021 (DFU Multi-Class Challenge)
- **Modality**: RGB Photography with multi-class tags (Infection, Ischemia, Both, None)
- **Origin**: MMU & NHS Foundation Trust
- **License**: Academic Research Agreement
- **Status in Prototype**: Format adapter implemented (`ml/data/loaders/dfuc2021.py`).

### 3. Medetec Medical Wound Database
- **Modality**: Chronic wound surface images with color balance and measurement references
- **Origin**: Medetec wound database
- **License**: Open academic demonstration
- **Status in Prototype**: Reference scale calibration benchmark adapter.

### 4. Synthetic Procedural Benchmark (`SYNTHETIC_DEMO`)
- **Modality**: Algorithmically rendered wound boundaries and calibration patterns
- **Origin**: Built-in procedural generator (`ml/preprocessing/synthetic.py`)
- **License**: Apache 2.0 / MIT
- **Status in Prototype**: Active and verified for automated unit testing, CI, and live UI demonstration. Clearly marked with `is_synthetic = True`.
