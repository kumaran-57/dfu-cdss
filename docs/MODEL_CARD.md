# Model Card: DFU-XAI Segmentation and Representation Models

## Model Details
- **Architecture**: SegFormer-B0 (Hierarchical Vision Transformer with lightweight MLP decode head) and U-Net baseline with ResNet34 encoder.
- **Model Versions**: `segformer_b0_v1.0`, `unet_baseline_v1.0`.
- **License**: Research Prototype License (Apache 2.0).

---

## Intended Use & Clinical Decision Support Scope
- **Intended Use**: Assisting qualified healthcare practitioners in tracking 2D ulcer surface area ($cm^2$), Feret length/width ($mm$), and longitudinal tissue composition trajectory across serial consultations.
- **Prohibited Use**: Autonomous clinical diagnosis, prescribing systemic antibiotic therapy, determining surgical margins for amputation without clinician review, or direct-to-consumer unsupervised diagnosis.

---

## Technical Performance & Limitations
- **Primary Metrics**: Dice Similarity Coefficient (DSC), Intersection-over-Union (IoU), 95th Percentile Hausdorff Distance (HD95), Mean Absolute Area Error ($cm^2$).
- **Uncertainty & Out-of-Distribution Handling**: Employs Monte Carlo (MC) Dropout to estimate per-pixel epistemic entropy. Cases exceeding the uncertainty threshold ($> 0.35$) automatically abstain and route to clinician review.
- **Environmental Constraint**: Calibrated area calculations are disabled when no valid reference scale marker is detected.
