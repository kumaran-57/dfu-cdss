# Master of Engineering (ME) Dissertation Outline

**Title:** DFU-XAI: An Integrated Self-Supervised, Domain-Adaptive and Explainable AI Framework for Calibrated Longitudinal Diabetic Foot Ulcer Assessment and Monitoring

---

## Chapter 1: Introduction
- 1.1 Clinical Background & Burden of Diabetic Foot Ulcers
- 1.2 Limitations of Visual Assessment and Rulers in Clinical Practice
- 1.3 Machine Learning Decision Support & Challenges (Data scarcity, cross-device shift, trust)
- 1.4 Research Objectives & Scope
- 1.5 Thesis Structure

## Chapter 2: Literature Review & Related Work
- 2.1 Medical Image Segmentation (U-Net, Attention U-Net, Vision Transformers, SegFormer)
- 2.2 Self-Supervised Visual Representation Learning (SimCLR, DINOv2, MAE)
- 2.3 Domain Adaptation and Cross-Site Generalization
- 2.4 Multimodal Clinical Fusion (Tabular + Imaging)
- 2.5 Explainable AI (XAI) and Uncertainty Quantification in Healthcare

## Chapter 3: Research Methodology & Mathematical Formulation
- 3.1 Geometric Calibration & Planar Scale Estimation
- 3.2 Vision Transformer Segmentation Formulation
- 3.3 Epistemic Uncertainty Estimation via Monte Carlo Dropout
- 3.4 Longitudinal Trajectory Modeling via Mixed-Effects Regression
- 3.5 Multimodal Fusion Architecture

## Chapter 4: System Architecture & Software Engineering
- 4.1 Hybrid Mobile-Server Platform Architecture
- 4.2 Security, Role-Based Access Control, and HIPAA/GDPR Alignment
- 4.3 Database Schema & Relational Modeling
- 4.4 Automated Testing & Verification Pipeline

## Chapter 5: Experimental Evaluation & Results
- 5.1 Dataset Characterization & Ethical Governance
- 5.2 Experiment E1: Self-Supervised Representation Comparison
- 5.3 Experiment E2: Segmentation Performance (U-Net vs SegFormer-B0)
- 5.4 Experiment E5: Planar Scale Calibration Accuracy
- 5.5 Experiment E7: Multimodal Clinical Fusion
- 5.6 Experiment E8: Longitudinal Wound Trajectory Analysis
- 5.7 Experiment E9: Uncertainty Quantification & Abstention

## Chapter 6: Discussion, Limitations & Clinical Governance
- 6.1 Clinical Utility and Workflow Integration
- 6.2 Failure Mode Analysis
- 6.3 Technical & Ethical Limitations
- 6.4 Translation to Prospective Clinical Studies

## Chapter 7: Conclusion & Future Work
- 7.1 Summary of Contributions
- 7.2 Recommendations for Clinical Trial Deployment
