# Known Limitations & Clinical Boundary Ledger

This document maintains an honest, transparent account of current system capabilities, technical constraints, and clinical boundaries.

---

## 1. Clinical Boundaries & Decision Support Scope

1. **Not a Diagnostic Medical Device**:
   DFU-XAI is an exploratory research decision-support prototype. It is **not** certified as medical device software (e.g., FDA 510(k), CE mark under EU MDR). It does not autonomously diagnose diabetic foot ulcers, prescribe treatment plans, or instruct surgical debridement.
2. **Absence of 3D Volumetric Depth Sensing**:
   2D photographs from standard smartphone cameras cannot reliably measure wound depth or cavity undermining. Reported metrics are strictly 2D surface area ($cm^2$), maximum major length ($mm$), and maximum minor width ($mm$).
3. **Infection & Ischemia Cannot Be Diagnosed from RGB Photography Alone**:
   Superficial redness (erythema) from an ordinary smartphone photo is insufficient to differentiate colonization, superficial infection, deep cellulitis, or ischemia. Infection status, ABI/TBI, and osteomyelitis assessment must be entered by a licensed healthcare provider based on microbiological, clinical, and vascular evaluations.
4. **Area Reduction Does Not Guarantee Healing**:
   While percentage area reduction (PAR) over 2 to 4 weeks is an established clinical proxy, surface closure alone does not guarantee tissue durability or absence of deep abscess/re-ulceration.

---

## 2. Technical & Environmental Constraints

1. **Host Compute Architecture**:
   The current local development environment is a CPU-only workstation (AMD Ryzen 5 5600H, no NVIDIA GPU). Large-scale vision transformer pretraining (e.g., DINOv2 800M) requires distributed multi-GPU clusters.
2. **Synthetic Demonstration Fixtures**:
   In the absence of a signed Data Transfer Agreement (DTA) and Institutional Review Board (IRB) approval, the demo environment operates on procedurally generated synthetic wound images. Performance metrics computed on synthetic fixtures are for software verification only and must never be cited as real clinical accuracy.
3. **Lighting & Perspective Sensitivity**:
   Calibrated scale estimation assumes that the circular or rectangular reference marker is placed coplanar with the wound surface. Extreme oblique viewing angles (>30 degrees) introduce perspective distortion that requires multi-view rectification.
