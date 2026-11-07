# Automated Test Execution Report

**Date of Execution:** 2026-11-07  
**Test Framework:** Pytest 9.1.1 (Python 3.14.8 on Linux 7.1.5+kali-amd64 x86_64)  
**Execution Command:** `pytest backend/tests ml/tests -v` / `./scripts/run_tests.sh`  
**Overall Status:** **30 PASSED, 0 FAILED (100% Pass Rate)**

---

## Detailed Test Case Ledger

### Backend Services & Security
| Test Suite / File | Test Case Name | Result | Verification Scope |
| :--- | :--- | :---: | :--- |
| `test_health.py` | `test_root_endpoint` | **PASSED** | Service online status and clinical disclaimer display. |
| `test_health.py` | `test_health_api` | **PASSED** | Versioning, healthcheck, and safety warning. |
| `test_auth.py` | `test_login_success` | **PASSED** | Valid credentials return JWT bearer token and role. |
| `test_auth.py` | `test_login_invalid_password` | **PASSED** | Wrong password rejected with HTTP 401. |
| `test_auth.py` | `test_login_nonexistent_user` | **PASSED** | Unknown email rejected with HTTP 401. |
| `test_auth.py` | `test_get_current_user_profile`| **PASSED** | JWT token decoded and profile retrieved. |
| `test_auth.py` | `test_get_profile_unauthorized`| **PASSED** | Missing token rejected with HTTP 401/403. |
| `test_rbac.py` | `test_admin_can_create_user` | **PASSED** | Admin successfully provisions new clinician. |
| `test_rbac.py` | `test_clinician_cannot_create_user` | **PASSED** | Clinician role prevented from user creation (HTTP 403). |
| `test_rbac.py` | `test_viewer_cannot_register_participant` | **PASSED** | Viewer role prevented from writing participant (HTTP 403). |
| `test_rbac.py` | `test_clinician_can_register_participant` | **PASSED** | Clinician successfully creates study participant. |
| `test_participants_visits.py` | `test_participant_and_visit_lifecycle` | **PASSED** | Coded Study ID uniqueness, visit creation, and clinical observation recording. |
| `test_calibration_and_quality.py` | `test_manual_scale_calibration` | **PASSED** | Millimeter/pixel geometric scale calculation. |
| `test_calibration_and_quality.py` | `test_calibrated_area_calculation` | **PASSED** | Surface area calculation in metric $cm^2$. |
| `test_calibration_and_quality.py` | `test_uncalibrated_area_refusal` | **PASSED** | Refuses to report calibrated dimensions when uncalibrated. |
| `test_calibration_and_quality.py` | `test_blur_and_exposure_assessment` | **PASSED** | Laplacian sharpness variance and luminance checks. |
| `test_audit.py` | `test_audit_log_tracking_and_admin_view` | **PASSED** | Operations logged immutably and viewable by Admin. |
| `test_audit.py` | `test_non_admin_cannot_view_audit_logs` | **PASSED** | Clinicians prevented from audit inspection (HTTP 403). |
| `test_end_to_end_pipeline.py` | `test_full_clinical_pipeline_vertical_slice` | **PASSED** | Full workflow: Login -> Participant -> Visit -> Image Upload -> Blur Check -> Calibrate -> Segment -> Clinician Review -> Longitudinal Trajectory -> CSV Export. |

### Machine Learning & Scientific Evaluation
| Test Suite / File | Test Case Name | Result | Verification Scope |
| :--- | :--- | :---: | :--- |
| `test_metrics.py` | `test_dice_and_iou_exact_match` | **PASSED** | Identical binary masks evaluate to DSC = 1.0, IoU = 1.0. |
| `test_metrics.py` | `test_dice_and_iou_disjoint` | **PASSED** | Disjoint masks evaluate to DSC = 0.0, IoU = 0.0. |
| `test_metrics.py` | `test_dice_half_overlap` | **PASSED** | Mathematical accuracy on 50% overlapping regions. |
| `test_metrics.py` | `test_hd95_metric` | **PASSED** | 95th percentile Hausdorff Distance boundary comparison. |
| `test_metrics.py` | `test_brier_and_ece` | **PASSED** | Brier score and Expected Calibration Error for probability reliability. |
| `test_models.py` | `test_unet_inference_shape_and_metadata` | **PASSED** | U-Net baseline forward pass and tissue partition fractions. |
| `test_models.py` | `test_segformer_inference_shape_and_metadata`| **PASSED** | SegFormer-B0 forward pass and epistemic uncertainty score. |
| `test_manifest_leakage.py` | `test_valid_manifest_zero_leakage` | **PASSED** | Manifest validator confirms 100% patient partition isolation. |
| `test_manifest_leakage.py` | `test_patient_leakage_detection` | **PASSED** | Correctly catches and raises error on cross-split patient overlap. |
| `test_fusion_and_ssl.py` | `test_multimodal_fusion_ablation` | **PASSED** | Controlled 3-way ablation (Image-only vs Clinical-only vs Fused). |
| `test_fusion_and_ssl.py` | `test_ssl_encoder_feature_extraction_and_probing` | **PASSED** | Latent feature extraction and downstream linear probe classification. |

---

## Frontend Build Status
- **Next.js 14 Production Build**: **COMPILED & VERIFIED (Code 0)**
- **Routes Generated**:
  - `/` (Dashboard Overview)
  - `/login` (Role-based Authentication)
  - `/participants` (Participant Registry & Coded ID Search)
  - `/participants/[id]` (Longitudinal Timeline & Area Reduction Trajectory)
  - `/visits/[id]/capture` (Capture, Blur Check & Geometric Calibration)
  - `/visits/[id]/assessment` (AI Segmentation Overlay & Clinician Adjudication)
  - `/research` (Experiment Matrices E1–E10 & De-identified CSV Export)
