# DFU-XAI Machine Learning Experiment Plan

This plan formalizes experiments E1 through E10 as specified in the master research prompt.

---

## Experiment Matrix

| ID | Experiment Title | Experimental Comparison | Primary Evaluation Metrics |
| :--- | :--- | :--- | :--- |
| **E1** | SSL Visual Representation | ImageNet-pretrained vs DINOv2 vs SimCLR vs MAE backbones | Linear probing Macro-F1, ROC-AUC, PR-AUC |
| **E2** | Boundary Segmentation | Standard U-Net baseline vs SegFormer-B0 candidate | Dice Score (DSC), IoU, HD95 (mm) |
| **E3** | Label Efficiency | Downstream segmentation under 10%, 25%, 50%, 100% labeled masks | $\Delta$ Dice vs percentage of annotations |
| **E4** | Domain Adaptation | Unadapted baseline vs confidence-filtered pseudo-labeling | Target-site Dice, degradation gap ($\%$) |
| **E5** | Scale & Color Calibration | Uncalibrated pixel metrics vs calibrated mm/cm² measures | Mean Absolute Area Error ($cm^2$), ICC, Bland-Altman |
| **E6** | Tissue Granularity | Binary wound area only vs multi-class (granulation, slough, necrosis) | Multi-class Mean IoU, correlation with healing rate |
| **E7** | Clinical Feature Fusion | Image-only vs Clinical-only (HbA1c, neuropathy, ABI) vs Fused | Brier score, ROC-AUC, SHAP attribution rankings |
| **E8** | Longitudinal Progression | Single-visit snapshot vs Mixed-Effects Temporal Trajectory | Area change rate ($cm^2/\text{week}$), residual variance |
| **E9** | Calibrated Uncertainty | Deterministic inference vs MC Dropout Epistemic Uncertainty | Expected Calibration Error (ECE), Risk-Coverage curve |
| **E10** | Edge & Server Deployment | PyTorch native inference vs ONNX Runtime CPU inference | Latency ($ms$), peak memory usage (MB), numerical delta |

---

## Methodological Rules
- **Patient-Level Data Partitioning**: All images and serial visits from any single participant must reside exclusively within either Train, Validation, or Test sets to eliminate data leakage.
- **Held-Out Test Set**: The test partition is sealed until hyperparameter tuning is frozen.
