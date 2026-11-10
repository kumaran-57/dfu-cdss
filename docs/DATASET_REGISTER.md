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

### 4. Foot Ulcer Segmentation Challenge (FUSeg 2021 / UWM Big Data)
- **Modality**: RGB Clinical Photography with pixel-level ground truth binary wound segmentation masks (1,210+ images)
- **Origin**: Big Data Analytics and Visualization Lab, University of Wisconsin-Milwaukee (Prof. Zeyun Yu) & AZH Wound and Vascular Center, Milwaukee, WI
- **Repository**: [uwm-bigdata/wound-segmentation](https://github.com/uwm-bigdata/wound-segmentation) / [Zenodo DOI: 10.5281/zenodo.4575314](https://doi.org/10.5281/zenodo.4575314) / MICCAI 2021 Challenge
- **License / Terms**: Academic Non-Commercial Research & Challenge Benchmarking (CC BY-NC / Grand Challenge agreement)
- **Status in Prototype**: Format adapter and manifest builder implemented in [`ml/data/loaders/fuseg.py`](file:///home/devil/Documents/Projects/ME_Project/ml/data/loaders/fuseg.py). Compatible with SegFormer-B0 and U-Net training pipelines.
- **Suitability for DFU-XAI**: High. Directly provides boundary masks for DFU segmentation, suitable for training on Kaggle GPU.

### 5. Synthetic Procedural Benchmark (`SYNTHETIC_DEMO`)
- **Modality**: Algorithmically rendered wound boundaries and calibration patterns
- **Origin**: Built-in procedural generator (`ml/preprocessing/synthetic.py`)
- **License**: Apache 2.0 / MIT
- **Status in Prototype**: Active and verified for automated unit testing, CI, and live UI demonstration. Clearly marked with `is_synthetic = True`.
