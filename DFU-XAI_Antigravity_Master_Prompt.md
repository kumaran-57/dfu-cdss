# Antigravity Master Prompt --- DFU-XAI Full ME Project

> **Instruction:** Build the complete DFU-XAI research prototype in the
> currently open workspace. Work incrementally, inspect the existing
> repository before changing anything, and keep the project runnable at
> every major milestone. Do not fabricate datasets, clinical results,
> ethics approvals, citations, or model performance.

------------------------------------------------------------------------

## 1. Project identity

**Project title**

DFU-XAI: An Integrated Self-Supervised, Domain-Adaptive and Explainable
AI Framework for Calibrated Longitudinal Diabetic Foot Ulcer Assessment
and Monitoring

**Project objective**

Develop a research-grade, end-to-end prototype that supports
clinician-supervised diabetic foot ulcer (DFU) assessment using:

1.  Standardised smartphone wound-image capture and quality checks.
2.  Image scale and colour-reference calibration.
3.  Wound segmentation and calibrated wound measurement.
4.  Optional tissue-region segmentation when reliable annotations exist.
5.  A controlled comparison of self-supervised visual representation
    learning methods.
6.  Domain adaptation and cross-device robustness experiments.
7.  Fusion of image-derived measurements with structured clinical
    information.
8.  Patient-level longitudinal wound monitoring across visits.
9.  Explainability, uncertainty estimation and out-of-distribution
    warnings.
10. A secure hybrid deployment: smartphone/PWA capture with server-side
    AI inference.
11. Reproducible experiments, evaluation reports, documentation and a
    dissertation/paper support folder.

This is a **research and clinician decision-support prototype only**. It
must not diagnose, prescribe treatment, replace a clinician, or claim
clinical validation unless a properly approved study has actually been
completed.

## 2. Mandatory working rules

### 2.1 Inspect before implementation

-   Inspect the current workspace, repository, installed tools,
    operating system, available GPU/CPU, RAM, Python and Node versions.
-   Preserve useful existing code. Do not overwrite or delete existing
    files without first understanding their purpose.
-   If the repository is empty, create the structure described below.
-   Create `docs/PROJECT_STATUS.md` and update it at the end of every
    phase.
-   Create `docs/DECISIONS.md` to record important technical decisions,
    alternatives and reasons.
-   Create `docs/KNOWN_LIMITATIONS.md` and maintain it honestly.
-   Use small, testable implementation steps. Do not generate the entire
    application as one unverified code dump.

### 2.2 No fabricated data or results

-   Never invent patient records, wound photographs, annotations,
    clinical outcomes, citations, ethics approval, hospital
    partnerships, or model metrics.
-   Synthetic data may be used only for UI development, API tests and
    pipeline smoke tests. Clearly mark every synthetic record and image
    as synthetic.
-   Do not use synthetic data to claim model accuracy, clinical
    validity, healing prediction performance or publication results.
-   If no real dataset is present, implement the data loaders, schemas,
    training pipeline and demo mode, then report that real training is
    blocked pending lawful data access.
-   Do not scrape patient images or bypass dataset access controls.
-   Do not assume a dataset's licence permits model training,
    redistribution or publication. Record the source, licence, access
    conditions and permitted uses for every dataset.

### 2.3 Patient safety, privacy and ethics

-   Do not collect, import, transmit or process identifiable patient
    data until the relevant institutional ethics approval, hospital
    permission, informed consent and data-sharing requirements are in
    place.
-   Do not upload identifiable wound photographs or clinical records to
    public AI services, public repositories, unapproved cloud storage or
    GitHub.
-   Never commit patient data, secrets, API keys, access tokens,
    credentials or environment files.
-   Use coded research IDs. Store any identity-linking key separately
    under the institution's control.
-   Remove EXIF metadata from image copies used for research, while
    preserving required audit metadata separately in an approved secure
    system.
-   Warn users to exclude faces, name bands, labels and other
    identifiers from photographs.
-   Apply role-based access, least privilege, audit logging, secure
    session handling, encrypted transport and institution-approved
    encrypted storage.
-   Use secure temporary upload handling, file type and size validation,
    malware-safe processing practices and rate limits.
-   Do not log image bytes, clinical notes, tokens or other sensitive
    values.
-   Build privacy controls and documentation, but do not claim legal or
    regulatory compliance merely because features exist. Require
    institutional review.
-   Add a prominent notice in the UI: **"Research decision-support
    prototype. Not for autonomous diagnosis or treatment. Clinical
    decisions must be made by qualified healthcare professionals."**

### 2.4 Clinical safety boundaries

-   Do not infer infection, ischemia, osteomyelitis, neuropathy or
    vascular status from an ordinary photograph alone.
-   Infection, ischemia, neuropathy, ABI/TBI and wound grading must be
    entered as clinician-assessed data with source and date.
-   Do not generate treatment recommendations, medication advice,
    debridement instructions or autonomous triage decisions.
-   A worsening or uncertain result should be displayed as a
    **"clinician review required"** flag, not as a diagnosis.
-   A decreasing wound area alone does not prove healing.
-   Do not invent or use arbitrary weights for a new wound
    severity/progression score.
-   Do not predict an individual patient's healing time unless a
    sufficiently powered, approved and externally validated prognostic
    study supports it. The initial system should report measured trends
    and uncertainty.

------------------------------------------------------------------------

## 3. Preferred technology stack

Use stable, compatible versions and pin dependencies.

### Frontend

-   Next.js with TypeScript.
-   App Router.
-   Responsive, accessible UI suitable for desktop and mobile.
-   PWA support for capture and offline queuing.
-   A clean clinician dashboard and patient-visit timeline.
-   Use a maintained charting library for longitudinal charts.
-   Do not store sensitive patient data in browser local storage or
    IndexedDB in plaintext. If offline capture is implemented, use an
    approved encrypted storage approach and document the security
    assumptions. If secure local encryption cannot be implemented
    safely, disable offline storage and explain why.

### Backend

-   Python FastAPI.
-   Pydantic schemas.
-   SQLAlchemy or SQLModel.
-   PostgreSQL for structured data.
-   Alembic migrations.
-   Secure object storage abstraction for images; local storage only for
    development/demo.
-   Background task mechanism for model inference if needed.
-   OpenAPI documentation.
-   ONNX Runtime for production-style inference where supported; PyTorch
    for research training.

### Machine learning

-   PyTorch.
-   torchvision / timm as appropriate.
-   Hugging Face Transformers or official model implementations where
    licensing and compatibility permit.
-   OpenCV for image processing and calibration.
-   Segmentation implementation with SegFormer-B0 and U-Net baseline.
-   DINOv2, SimCLR and MAE representation-learning experiments.
-   LightGBM and scikit-learn for structured clinical baselines.
-   SHAP and Grad-CAM-compatible tooling.
-   Deep ensembles or MC Dropout for uncertainty experiments.
-   ONNX export and validation.

### Engineering

-   Docker Compose for local development.
-   `.env.example` with placeholders only.
-   Ruff/Black or a consistent Python formatter/linter.
-   ESLint/Prettier for frontend.
-   Pytest for backend and ML tests.
-   Playwright or an equivalent browser test framework for frontend
    flows.
-   GitHub Actions CI with lint, type checks and tests; never include
    patient data in CI.

If a dependency is unavailable or incompatible, document the issue and
select a maintained alternative. Do not silently replace a research
method with a different one.

------------------------------------------------------------------------

## 4. Required repository structure

Create or adapt the following structure. Keep the repository
understandable and avoid unnecessary microservices.

``` text
dfu-xai/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docker-compose.yml
├── docs/
│   ├── PROJECT_STATUS.md
│   ├── DECISIONS.md
│   ├── KNOWN_LIMITATIONS.md
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── DATA_DICTIONARY.md
│   ├── DATA_GOVERNANCE.md
│   ├── ETHICS_AND_CONSENT_CHECKLIST.md
│   ├── DATASET_REGISTER.md
│   ├── ANNOTATION_GUIDELINES.md
│   ├── MODEL_CARD.md
│   ├── THREAT_MODEL.md
│   ├── API_GUIDE.md
│   ├── USER_GUIDE.md
│   ├── TEST_REPORT.md
│   ├── EXPERIMENT_PLAN.md
│   ├── RESULTS_TEMPLATE.md
│   ├── PUBLICATION_PLAN.md
│   └── DISSERTATION_OUTLINE.md
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── hooks/
│   ├── public/
│   ├── tests/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── security/
│   │   └── storage/
│   ├── migrations/
│   ├── tests/
│   └── pyproject.toml
├── ml/
│   ├── configs/
│   ├── data/
│   │   ├── manifests/
│   │   ├── loaders/
│   │   └── validation/
│   ├── preprocessing/
│   ├── calibration/
│   ├── models/
│   │   ├── encoders/
│   │   ├── segmentation/
│   │   ├── fusion/
│   │   ├── longitudinal/
│   │   └── uncertainty/
│   ├── explainability/
│   ├── training/
│   ├── evaluation/
│   ├── export/
│   ├── scripts/
│   └── tests/
├── experiments/
│   ├── configs/
│   ├── logs/
│   ├── reports/
│   └── README.md
├── research/
│   ├── literature_matrix.csv
│   ├── protocol/
│   ├── crf/
│   ├── analysis/
│   └── manuscript/
├── data/
│   ├── README.md
│   ├── sample_synthetic/
│   └── .gitkeep
└── scripts/
    ├── setup_dev.sh
    ├── check_environment.py
    ├── run_tests.sh
    └── validate_dataset.py
```

Do not put real patient images or real clinical records inside the Git
repository. The `data/` folder should contain only documentation, empty
directories and explicitly synthetic demo assets.

------------------------------------------------------------------------

## 5. Functional requirements

### 5.1 Authentication and roles

Implement secure authentication and at least these roles:

-   `admin`: manages users, roles and system configuration.
-   `clinician`: can access authorised patient records, review
    assessments and enter clinical findings.
-   `researcher`: can access only approved, coded research data and
    aggregate results.
-   `viewer`: read-only access to explicitly authorised records.

Requirements:

-   Enforce permissions on the backend, not only by hiding frontend
    routes.
-   Prevent users from changing their own role.
-   Use secure password hashing or a well-maintained authentication
    provider approved by the deployment institution.
-   Use secure, HttpOnly, SameSite cookies where appropriate.
-   Add session expiry, logout, account lockout/rate limiting and audit
    logs.
-   Provide no default production admin password. Use a documented
    one-time bootstrap process.
-   Add tests for privilege escalation and unauthorised record access.

### 5.2 Patient and visit management

Create coded research participant records with:

-   Study ID (unique, non-identifying).
-   Demographic fields approved by the study protocol.
-   Consent status and consent version/date.
-   Enrolment status.
-   Created/updated timestamps.
-   Access-control and audit metadata.

Create visits linked to a participant:

-   Visit ID.
-   Study ID.
-   Visit date/time.
-   Wound side and anatomical location.
-   Clinical observations and their source.
-   Treatment/offloading notes entered by authorised clinicians.
-   Follow-up status.
-   Image and annotation references.

Avoid collecting unnecessary identifiers. Keep direct identifiers out of
the research schema.

### 5.3 Smartphone image capture

Build a mobile-friendly capture workflow:

-   Request camera permission only when the user starts capture.
-   Explain how to frame the wound and reference card.
-   Allow capture or upload of supported image types.
-   Validate file size, MIME type and actual image decoding.
-   Detect blur, severe under/overexposure and inadequate framing.
-   Display quality feedback and allow recapture.
-   Capture device make/model only if justified and approved.
-   Remove image metadata from the research copy.
-   Show a warning if a scale or colour reference is missing.
-   Do not automatically claim that perspective, depth or colour has
    been corrected when it has not.
-   Support multiple images per visit with view labels.
-   Do not use images of real people in the demo. Use clearly synthetic
    placeholders or user-provided, authorised assets.

### 5.4 Image calibration and measurement

Implement a modular calibration pipeline:

1.  Detect or allow manual selection of a known-size reference marker.
2.  Estimate pixel-to-mm scale.
3.  Check whether the reference plane is sufficiently aligned with the
    wound plane.
4.  Detect a supported colour reference chart if available.
5.  Apply documented colour correction only when calibration conditions
    are met.
6.  Record calibration method, parameters and quality flags.
7.  Refuse to report calibrated dimensions when calibration fails.
8.  Store raw and processed-image references separately under controlled
    access.

Outputs:

-   Wound mask.
-   Pixel area.
-   Calibrated area in cm² only when valid calibration is available.
-   Length/width estimates with a documented method.
-   Perimeter and shape descriptors where useful.
-   Calibration confidence/quality status.

Do not present estimated wound depth from a 2D photograph.

### 5.5 Segmentation

Implement:

-   U-Net baseline.
-   SegFormer-B0 primary candidate.
-   Binary wound segmentation as the minimum viable task.
-   Optional tissue segmentation classes: granulation, slough and
    necrotic tissue, only when adequate expert labels are available.
-   Configurable class mapping for each dataset.
-   Dataset-specific label conversion documented in code and docs.
-   Dice, IoU and HD95 evaluation.
-   Overlay visualisation with a legend.
-   Save model version and inference configuration with each prediction.

Never use an image-level classification label as if it were a
pixel-level segmentation mask.

### 5.6 Self-supervised learning comparison

Implement a reproducible experiment framework for:

-   DINOv2.
-   SimCLR.
-   MAE.
-   ImageNet-supervised baseline.

Requirements:

-   Use identical patient-level train/validation/test partitions.
-   Keep data augmentation clinically safe and document each transform.
-   Avoid horizontal/vertical flips or colour transformations if they
    would invalidate laterality, tissue appearance or calibration
    assumptions; justify any augmentation used.
-   Support frozen-encoder and fine-tuned experiments.
-   Record random seeds, model/checkpoint identifiers, training
    configuration, data manifest hash, software versions and hardware.
-   Compare downstream segmentation and/or classification under multiple
    labelled-data fractions where feasible.
-   Report mean and confidence intervals across repeated seeds when
    compute allows.
-   Do not claim one SSL method is superior until the experiment has
    been run.

If pretrained weights require a licence or download approval, document
that and provide a configuration switch rather than bypassing
restrictions.

### 5.7 Domain adaptation and cross-device evaluation

Implement a controlled, optional domain-adaptation experiment:

-   Baseline: source-domain training without adaptation.
-   Adapted: a documented target-domain adaptation method, such as
    confidence-filtered self-training with pseudo-label quality checks.
-   Keep target test data completely held out.
-   Never use target test labels for training or threshold selection.
-   Track pseudo-label confidence thresholds and the number of
    accepted/rejected pseudo-labels.
-   Report performance by source, hospital/site and camera/device where
    available.
-   Provide a no-adaptation baseline.
-   Do not claim domain adaptation is novel by itself.

### 5.8 Clinical feature fusion

Implement a structured clinical data pipeline with:

-   Explicit units and allowable ranges.
-   Measurement date and source for each variable.
-   Missing-value indicators.
-   No silent imputation.
-   Training-only fitting of imputation, scaling and feature selection.
-   Logistic regression baseline.
-   LightGBM candidate.
-   Image-only, clinical-only and fused comparisons.
-   Feature importance/SHAP explanations.
-   A clear record of which variables were available at prediction time.

Potential variables, subject to ethics approval and clinical protocol:

-   Age and sex.
-   Diabetes type and duration.
-   HbA1c and date.
-   BMI.
-   Neuropathy assessment.
-   Vascular findings, ABI/TBI if available.
-   Previous ulcer/amputation history.
-   Wound duration, location and clinician-assigned classification.
-   Treatment/offloading information.

Do not include variables recorded after the prediction time in a model
intended to predict an earlier outcome. Prevent target leakage.

### 5.9 Longitudinal analysis

Support multiple visits for the same coded participant and wound.

Compute and display:

-   Area per visit.
-   Percentage area change from baseline.
-   Area change rate with elapsed time.
-   Tissue composition proportions where validated.
-   Changes in shape/boundary.
-   Clinical assessment and treatment changes.
-   Missing-visit indicators.
-   Measurement quality and uncertainty.

Use mixed-effects regression or other appropriate patient-level
statistical methods as the initial longitudinal baseline. Compare:

1.  Single-visit baseline.
2.  Area-only temporal features.
3.  Area + tissue temporal features.
4.  Image + clinical + temporal features.

Do not train a deep temporal model by default. Add an LSTM/Transformer
only if sample size, number of repeated visits and independent outcome
events justify it.

Display a timeline with a clear statement that measured area reduction
alone is not proof of healing. Any progression category must be based on
a documented, clinician-reviewed definition.

### 5.10 Explainability and uncertainty

Implement:

-   Segmentation mask overlays.
-   Grad-CAM for supported classification/encoder outputs.
-   SHAP for structured clinical models.
-   Prediction confidence and calibrated probability where applicable.
-   Deep ensemble or MC Dropout uncertainty experiment.
-   Out-of-distribution/image-quality warning where feasible.
-   A configurable abstention rule that routes uncertain cases to
    clinician review.

Explainability visualisations are supporting information, not proof that
the model is correct. Add this limitation to the UI and model card.

### 5.11 Clinician dashboard

Build a professional, responsive dashboard containing:

-   Overview of authorised participants and visits.
-   Search by coded study ID.
-   Participant profile and visit timeline.
-   Image viewer with original/processed toggle.
-   Wound mask overlay and tissue legend.
-   Measurement summary and calibration status.
-   Longitudinal charts.
-   Clinical observations and treatment notes.
-   AI output with model version, uncertainty and warnings.
-   Clinician review/override fields with reason and timestamp.
-   Exportable PDF research report with a clear research-only
    disclaimer.

Do not show identifiable patient records to a researcher or viewer
unless explicitly authorised.

### 5.12 Research data export

Implement controlled exports:

-   De-identified CSV for approved tabular data.
-   Annotation and image manifest export without embedding images by
    default.
-   Dataset split manifest.
-   Model predictions with model version and timestamps.
-   Export audit log.
-   Export permissions and confirmation.
-   No public sharing or automatic upload.

------------------------------------------------------------------------

## 6. Database design

Design and document a relational schema. At minimum include:

-   `users`
-   `roles` or role assignments
-   `participants`
-   `consent_records`
-   `visits`
-   `wounds`
-   `clinical_observations`
-   `images`
-   `annotations`
-   `calibration_records`
-   `model_versions`
-   `predictions`
-   `longitudinal_measurements`
-   `clinician_reviews`
-   `audit_logs`
-   `dataset_sources`

Use UUIDs or similarly non-guessable internal identifiers. Enforce
foreign keys, constraints, indexes and transaction boundaries. Store
units, source, timestamps and missingness explicitly. Use database
migrations. Do not put image binaries directly in ordinary relational
rows unless there is a specific, justified reason.

Provide an ER diagram in `docs/SYSTEM_ARCHITECTURE.md` using Mermaid.

------------------------------------------------------------------------

## 7. API requirements

Implement and document versioned REST endpoints. Suggested groups:

### Authentication

-   `POST /api/v1/auth/login`
-   `POST /api/v1/auth/logout`
-   `GET /api/v1/auth/me`

### Participants and visits

-   `GET /api/v1/participants`
-   `POST /api/v1/participants`
-   `GET /api/v1/participants/{id}`
-   `POST /api/v1/participants/{id}/visits`
-   `GET /api/v1/participants/{id}/visits`

### Images

-   `POST /api/v1/visits/{visit_id}/images`
-   `GET /api/v1/images/{image_id}/metadata`
-   `POST /api/v1/images/{image_id}/quality-check`
-   `POST /api/v1/images/{image_id}/calibrate`

### AI assessment

-   `POST /api/v1/images/{image_id}/segment`
-   `POST /api/v1/images/{image_id}/assess`
-   `GET /api/v1/predictions/{prediction_id}`

### Longitudinal and review

-   `GET /api/v1/participants/{id}/progression`
-   `POST /api/v1/predictions/{id}/clinician-review`

### Research administration

-   `GET /api/v1/research/metrics`
-   `POST /api/v1/research/exports`

For every endpoint:

-   Define Pydantic request/response schemas.
-   Enforce authentication and role-based access.
-   Validate ownership/authorisation for every referenced record.
-   Return safe error messages.
-   Add pagination and filtering where appropriate.
-   Add tests for successful and forbidden requests.
-   Never expose internal file paths, stack traces, secrets or sensitive
    clinical data in errors.

------------------------------------------------------------------------

## 8. Machine-learning experiment plan

Create YAML/JSON configs and scripts for these experiments.

  ------------------------------------------------------------------------
  ID                      Experiment              Comparison
  ----------------------- ----------------------- ------------------------
  E1                      SSL representation      ImageNet vs DINOv2 vs
                                                  SimCLR vs MAE

  E2                      Segmentation            U-Net vs SegFormer-B0

  E3                      Label efficiency        10%, 25%, 50%, 100%
                                                  labelled training data,
                                                  if sample size permits

  E4                      Domain adaptation       No adaptation vs
                                                  confidence-filtered
                                                  adaptation

  E5                      Calibration             Uncalibrated vs
                                                  scale/colour calibrated

  E6                      Tissue contribution     Area-only vs area +
                                                  tissue

  E7                      Clinical fusion         Image-only vs
                                                  clinical-only vs fused

  E8                      Temporal contribution   Single visit vs serial
                                                  visit features

  E9                      Uncertainty             Standard output vs
                                                  calibrated
                                                  uncertainty/abstention

  E10                     Deployment              PyTorch vs ONNX
                                                  inference latency and
                                                  memory
  ------------------------------------------------------------------------

### Evaluation requirements

-   Patient-level data splits; all visits and images from a participant
    stay in one partition.
-   Keep a final test set untouched until model selection is complete.
-   Prefer external site/device validation if legitimately available.
-   Report sensitivity, specificity, macro-F1, ROC-AUC and PR-AUC for
    classification tasks.
-   Report Dice, IoU and HD95 for segmentation.
-   Report MAE, percentage error, ICC and Bland--Altman analysis for
    measurements.
-   Report ECE and Brier score for calibration.
-   Report risk--coverage curves for selective prediction.
-   Report confidence intervals and class counts.
-   Document class imbalance and missing data.
-   Do not report only accuracy.
-   Do not claim clinical benefit from retrospective technical metrics
    alone.
-   Include subgroup and device-level performance where sample sizes
    permit.
-   Record failed runs and negative results rather than hiding them.

Create scripts such as:

``` bash
python -m ml.scripts.validate_dataset --manifest path/to/manifest.csv
python -m ml.scripts.train_segmentation --config ml/configs/segformer_baseline.yaml
python -m ml.scripts.run_ssl_comparison --config experiments/configs/ssl_comparison.yaml
python -m ml.scripts.evaluate --config experiments/configs/evaluation.yaml
python -m ml.scripts.export_onnx --model-path path/to/checkpoint
```

Adapt commands to the actual implemented module names and document the
final commands. Do not leave fake commands in the README.

------------------------------------------------------------------------

## 9. Dataset manifest and annotation protocol

Create a manifest format with fields such as:

-   `image_id`
-   `participant_code`
-   `wound_code`
-   `visit_code`
-   `image_path` (relative path outside Git)
-   `dataset_source`
-   `licence_or_permission`
-   `site_code`
-   `device_code`
-   `capture_date` (appropriately de-identified)
-   `view_type`
-   `label_status`
-   `annotation_path`
-   `split`
-   `consent_or_access_basis`
-   `quality_status`

Do not put names, phone numbers, addresses, hospital numbers or direct
identifiers in the manifest.

Create `docs/ANNOTATION_GUIDELINES.md` specifying:

-   Wound-boundary definition.
-   Tissue-class definitions agreed with a clinician.
-   Handling of uncertain boundaries.
-   Handling of occlusion and poor image quality.
-   Annotation format and version.
-   Independent review/adjudication process.
-   Inter-annotator agreement procedure.
-   Rules for excluding unusable images.

Do not invent clinical annotation definitions. Mark items requiring
clinician approval.

------------------------------------------------------------------------

## 10. Frontend screens

Implement these screens with realistic but explicitly synthetic demo
content:

1.  Login.
2.  Role-specific landing page.
3.  Dashboard overview.
4.  Participant list.
5.  Add participant (coded research ID only).
6.  Participant detail.
7.  Add visit.
8.  Smartphone camera/upload capture.
9.  Image quality and calibration review.
10. Wound segmentation and measurement result.
11. Longitudinal progression timeline.
12. Clinical data entry.
13. Clinician review.
14. Research experiment/results dashboard.
15. User and role administration.
16. Audit log viewer for authorised administrators.
17. Settings and data-governance information.

UI requirements:

-   Professional medical research dashboard, not a consumer diagnosis
    app.
-   Accessible contrast, keyboard navigation, clear labels and
    responsive layouts.
-   Use neutral, restrained colours.
-   Distinguish measured values, clinician-entered values and
    AI-generated estimates.
-   Display units and timestamps.
-   Display model version and calibration status.
-   Show missing or unavailable information honestly.
-   Confirm destructive actions.
-   Do not use fake testimonials, fake hospital logos or fake clinical
    endorsements.

------------------------------------------------------------------------

## 11. Testing and security

Create automated tests for:

### Backend

-   Authentication and session expiry.
-   Role permissions and privilege escalation.
-   Participant/visit access boundaries.
-   Upload validation and malicious file handling.
-   Database constraints and migrations.
-   Missing/invalid clinical values.
-   Calibration failure handling.
-   AI service unavailable/error handling.
-   Audit logging.
-   Export permissions.

### ML

-   Dataset leakage checks.
-   Patient-level split checks.
-   Label mapping correctness.
-   Empty-mask and invalid-mask handling.
-   Reproducibility and seed handling.
-   Metric calculations.
-   Calibration and uncertainty calculations.
-   ONNX vs PyTorch numerical consistency within a documented tolerance.
-   No prediction when model weights are missing; return a clear
    unavailable status.

### Frontend

-   Login and logout.
-   Role-specific navigation.
-   Camera permission denial.
-   Invalid file upload.
-   Failed network and retry behaviour.
-   Visit timeline.
-   Measurement and uncertainty display.
-   Clinician review.
-   Responsive layouts and accessibility basics.

### Security

-   Check for hardcoded secrets.
-   Check unsafe CORS configuration.
-   Check missing backend authorization.
-   Check insecure direct object references.
-   Check SQL injection risks and unsafe file paths.
-   Check upload size/type validation.
-   Check sensitive data in logs.
-   Check debug mode and development credentials.
-   Check dependency vulnerabilities using available local tools.
-   Do not perform intrusive testing against external systems.

Produce `docs/TEST_REPORT.md` with test commands, pass/fail results,
known gaps and remediation status. Never claim a test passed unless it
was actually run.

------------------------------------------------------------------------

## 12. Documentation and research outputs

Write clear, complete documentation:

### `README.md`

-   Project purpose and limitations.
-   Architecture summary.
-   Prerequisites.
-   Setup instructions.
-   Environment configuration.
-   Database setup/migrations.
-   Running frontend/backend.
-   Running tests.
-   Demo mode.
-   Dataset setup.
-   Training and evaluation commands.
-   Security and ethics warning.
-   Troubleshooting.

### `docs/EXPERIMENT_PLAN.md`

Document research questions, hypotheses, baselines, ablations, splits,
metrics and statistical methods.

### `docs/MODEL_CARD.md`

Document intended use, prohibited use, training data provenance,
limitations, evaluation, subgroup gaps, uncertainty and model version.

### `docs/DATA_GOVERNANCE.md`

Document consent basis, access controls, de-identification, retention,
deletion, export, backup and incident response procedures for
institutional approval.

### `docs/PUBLICATION_PLAN.md`

Create a realistic publication plan. Do not guarantee Scopus indexing,
acceptance or publication without fees. Include a checklist for
verifying journal indexing, scope, APC, waiver conditions and publisher
legitimacy at submission time.

### `research/manuscript/`

Create a manuscript skeleton with: - Abstract - Introduction - Related
work - Research gap - Materials and methods - Dataset and ethics -
Proposed architecture - Experimental setup - Results (empty template
until real experiments run) - Discussion - Limitations - Conclusion -
References

Do not fabricate citations. Use a reference manager export or verified
bibliographic metadata. Mark unverified references clearly.

------------------------------------------------------------------------

## 13. Development sequence and acceptance criteria

Work in the following order. Do not skip ahead if the current phase is
broken.

### Milestone 0 --- Repository and environment audit

-   Inspect workspace and hardware.
-   Record available GPU/CPU and memory.
-   Create project status, decisions and limitations docs.
-   Confirm the intended stack and dependency compatibility.

**Acceptance:** environment report and clean project structure.

### Milestone 1 --- Backend foundation

-   FastAPI app.
-   Database models and migrations.
-   Authentication and roles.
-   Health endpoint.
-   API tests.

**Acceptance:** backend starts, database migration works, auth and
access-control tests pass.

### Milestone 2 --- Frontend foundation

-   Next.js app.
-   Login and role-based shell.
-   Dashboard, participant and visit pages.
-   API client and error handling.

**Acceptance:** frontend runs and core navigation works.

### Milestone 3 --- Data and image pipeline

-   Dataset manifest validation.
-   Upload validation.
-   Image quality checks.
-   Metadata removal.
-   Calibration interface and service.
-   Synthetic demo fixtures clearly marked.

**Acceptance:** valid demo image can pass through the pipeline;
invalid/un-calibrated images are handled safely.

### Milestone 4 --- Segmentation baseline

-   U-Net baseline.
-   SegFormer-B0.
-   Training/evaluation scripts.
-   Overlay viewer.
-   Metrics and tests.

**Acceptance:** pipeline runs on an explicitly permitted dataset or
reports exactly what access is missing.

### Milestone 5 --- SSL comparison

-   DINOv2, SimCLR and MAE experiment adapters.
-   ImageNet baseline.
-   Reproducible configs and logs.
-   Fair comparison report template.

**Acceptance:** each method can be run or is clearly marked blocked by a
missing checkpoint, dependency, dataset or compute resource. Never
invent results.

### Milestone 6 --- Clinical and longitudinal analysis

-   Clinical schema and validation.
-   Image-only/clinical-only/fusion baselines.
-   Patient-level visit aggregation.
-   Mixed-effects analysis.
-   Longitudinal dashboard.

**Acceptance:** synthetic tests demonstrate correct calculations; real
clinical analysis remains blocked until approved data exists.

### Milestone 7 --- XAI, uncertainty and domain adaptation

-   Grad-CAM/SHAP.
-   Uncertainty and abstention.
-   Domain adaptation experiment.
-   Device/source evaluation.

**Acceptance:** visualisations and reliability outputs are tested and
limitations are documented.

### Milestone 8 --- Hybrid deployment

-   PWA capture.
-   Secure upload queue or explicitly disabled offline storage.
-   FastAPI inference endpoints.
-   ONNX export where supported.
-   PDF report.
-   Deployment configuration.

**Acceptance:** end-to-end demo works with synthetic data and no patient
data.

### Milestone 9 --- Final validation and handover

-   Run all tests.
-   Run security checks.
-   Review all documentation.
-   Verify no sensitive files or secrets are committed.
-   Create a final implementation report.

**Acceptance:** reproducible setup, documented commands, working demo,
test report, known limitations and clear list of items requiring
hospital data/ethics approval.

------------------------------------------------------------------------

## 14. Required final report

At completion, create `docs/FINAL_IMPLEMENTATION_REPORT.md` containing:

1.  What was implemented.
2.  Architecture and component descriptions.
3.  Repository structure.
4.  Environment and hardware used.
5.  Setup and run commands.
6.  Database schema and migrations.
7.  API endpoint summary.
8.  ML models implemented versus planned.
9.  Dataset sources and licence/access status.
10. Experiments actually executed.
11. Results actually obtained, with confidence intervals where
    available.
12. Tests run and their real outcomes.
13. Security review findings.
14. Known limitations and blocked work.
15. Items requiring clinician, hospital or ethics approval.
16. Recommended next steps.

Also create `docs/PROJECT_STATUS.md` with a checklist of completed,
partially completed, blocked and not-started tasks.

------------------------------------------------------------------------

## 15. Instructions for autonomous agent behaviour

-   Act as a senior full-stack engineer, ML researcher, MLOps engineer
    and security-conscious technical lead.
-   Plan before coding, but do not spend the entire task producing
    plans.
-   Implement a working vertical slice first: login → coded participant
    → visit → synthetic image upload → quality check → baseline
    segmentation/demo result → longitudinal display.
-   Then extend it with the research experiments.
-   Use real, maintainable code rather than placeholder functions for
    core functionality.
-   If a model or dataset cannot be downloaded or accessed, implement a
    clean adapter and document the blocker. Do not silently substitute a
    fake model.
-   Never fabricate predictions. If no trained model is installed, show
    "Model not configured" or "Demo output --- synthetic data".
-   Keep configuration separate from code.
-   Make commands reproducible.
-   Do not use arbitrary clinical thresholds. Any clinical threshold
    must be sourced, clinician-approved and configurable.
-   Do not use the final test set for tuning.
-   Do not claim prospective validation, clinical effectiveness,
    regulatory compliance, Scopus publication readiness or novelty
    without evidence.
-   Ask for user input only when an essential decision cannot be safely
    or reasonably made. Otherwise choose a sensible default, document it
    and continue.
-   After each milestone, run relevant tests and update
    `docs/PROJECT_STATUS.md`.
-   If the available environment cannot support training large models,
    build the pipeline so training can run later on suitable hardware;
    do not pretend training occurred.
-   Keep the application usable even when AI weights are unavailable by
    providing a clearly labelled synthetic demo mode.

## 16. Start now

Begin with **Milestone 0**:

1.  Inspect the current workspace and existing code.
2.  Check available hardware, GPU, memory, Python, Node and package
    managers.
3.  Identify existing files that must be preserved.
4.  Create `docs/PROJECT_STATUS.md`, `docs/DECISIONS.md` and
    `docs/KNOWN_LIMITATIONS.md`.
5.  Create or adapt the repository structure.
6.  Report the environment findings and a concise execution plan.
7.  Immediately proceed to Milestone 1 unless a genuine blocker requires
    my decision.

**The final goal is a secure, reproducible, end-to-end DFU-XAI research
prototype with honest experimental reporting---not a visually impressive
application containing fake AI results.**
