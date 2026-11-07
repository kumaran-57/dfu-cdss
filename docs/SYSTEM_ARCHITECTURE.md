# DFU-XAI System Architecture & Data Model

## 1. High-Level Architecture Overview

DFU-XAI is designed as a secure, hybrid medical decision-support platform separating presentation, API orchestration, and machine learning computation:

```mermaid
graph TD
    subgraph Frontend ["Client Tier (Next.js 14 App Router)"]
        UI_Dash[Clinician Dashboard]
        UI_Capture[PWA Smartphone Capture]
        UI_Timeline[Longitudinal Progression View]
        UI_Admin[Audit & Admin Console]
        UI_Research[Research & Export Portal]
    end

    subgraph Backend ["Application Tier (FastAPI REST Server)"]
        API_GW[FastAPI Router /api/v1]
        Auth_SVC[RBAC & Auth Service (JWT / Argon2)]
        Img_SVC[Image Validation & EXIF Stripper]
        Calib_SVC[Calibration & Scale Estimation]
        Seg_SVC[Segmentation & Metric Inference]
        Long_SVC[Longitudinal Modeling Engine]
        Audit_SVC[Audit Trail Logger]
        Storage_SVC[Secure De-identified Object Storage]
    end

    subgraph DataTier ["Persistence Tier"]
        DB[(Relational DB: SQLite / PostgreSQL)]
        DiskStore[(Encrypted Filesystem / S3 Blob Store)]
    end

    subgraph MLTier ["ML Experimentation & Inference Tier"]
        SegFormer[SegFormer-B0 Head]
        UNet[U-Net Baseline]
        SSL_Exp[SSL Harness: DINOv2 / SimCLR / MAE]
        Fusion_M[Clinical Fusion: LightGBM / Logistic]
        XAI_Engine[Grad-CAM & SHAP Attributions]
        Uncertainty[MC Dropout / Calibrated Abstention]
    end

    UI_Dash -->|HTTPS / REST| API_GW
    UI_Capture -->|Secure Upload| API_GW
    UI_Timeline -->|REST / JSON| API_GW
    UI_Admin -->|REST / JSON| API_GW
    UI_Research -->|REST / JSON| API_GW

    API_GW --> Auth_SVC
    API_GW --> Img_SVC
    API_GW --> Calib_SVC
    API_GW --> Seg_SVC
    API_GW --> Long_SVC
    API_GW --> Audit_SVC

    Auth_SVC --> DB
    Img_SVC --> Storage_SVC
    Storage_SVC --> DiskStore
    Seg_SVC --> SegFormer
    Seg_SVC --> UNet
    Seg_SVC --> Uncertainty
    Long_SVC --> Fusion_M
    API_GW --> XAI_Engine
```

---

## 2. Relational Database Entity-Relationship (ER) Diagram

The system employs a normalized, audit-compliant relational schema:

```mermaid
erDiagram
    USERS ||--o{ AUDIT_LOGS : triggers
    USERS ||--o{ CLINICIAN_REVIEWS : performs
    PARTICIPANTS ||--o{ CONSENT_RECORDS : holds
    PARTICIPANTS ||--o{ VISITS : attends
    VISITS ||--o{ WOUNDS : contains
    VISITS ||--o{ CLINICAL_OBSERVATIONS : records
    VISITS ||--o{ IMAGES : captures
    IMAGES ||--o{ CALIBRATION_RECORDS : has
    IMAGES ||--o{ ANNOTATIONS : has
    IMAGES ||--o{ PREDICTIONS : generates
    PREDICTIONS ||--o{ CLINICIAN_REVIEWS : receives
    PREDICTIONS ||--o{ LONGITUDINAL_MEASUREMENTS : contributes
    DATASET_SOURCES ||--o{ IMAGES : originates

    USERS {
        uuid id PK
        string email UK
        string hashed_password
        string role "admin | clinician | researcher | viewer"
        boolean is_active
        datetime created_at
    }

    PARTICIPANTS {
        uuid id PK
        string study_id UK "e.g. PART-001"
        string biological_sex
        int age_at_enrollment
        string enrollment_status
        datetime created_at
        datetime updated_at
    }

    CONSENT_RECORDS {
        uuid id PK
        uuid participant_id FK
        string consent_version
        string status "granted | withdrawn"
        datetime consent_date
        string verified_by_clinician_id
    }

    VISITS {
        uuid id PK
        uuid participant_id FK
        string visit_code "e.g. V01, V02"
        datetime visit_date
        int follow_up_day
        string notes
    }

    WOUNDS {
        uuid id PK
        uuid visit_id FK
        string wound_code "e.g. W1"
        string anatomical_location "plantar_forefoot | heel | dorsal"
        string laterality "left | right"
    }

    CLINICAL_OBSERVATIONS {
        uuid id PK
        uuid visit_id FK
        float hba1c_percentage
        datetime hba1c_date
        boolean neuropathy_present
        float abi_index
        string infection_status "none | superficial | deep"
        string offloading_modality "TCC | removable_boot | shoe"
        string observation_source "clinician_entered"
    }

    IMAGES {
        uuid id PK
        uuid visit_id FK
        string file_path
        string mime_type
        int width
        int height
        string sha256_hash
        string view_angle "perpendicular | oblique"
        boolean quality_passed
        float blur_score
        string exposure_status "normal | underexposed | overexposed"
        boolean is_synthetic
        datetime captured_at
    }

    CALIBRATION_RECORDS {
        uuid id PK
        uuid image_id FK
        string marker_type "circle_10mm | checkerboard_20mm | manual"
        float mm_per_pixel
        float calibration_confidence
        boolean color_card_detected
        datetime calibrated_at
    }

    PREDICTIONS {
        uuid id PK
        uuid image_id FK
        string model_version "segformer_v1 | unet_v1"
        string mask_path
        int pixel_area
        float calibrated_area_cm2
        float major_length_mm
        float minor_width_mm
        float granulation_percentage
        float slough_percentage
        float necrotic_percentage
        float uncertainty_score
        boolean review_flag
        datetime created_at
    }

    CLINICIAN_REVIEWS {
        uuid id PK
        uuid prediction_id FK
        uuid clinician_id FK
        boolean approved
        string override_notes
        float corrected_area_cm2
        datetime reviewed_at
    }

    AUDIT_LOGS {
        uuid id PK
        uuid user_id FK
        string action "LOGIN | RECORD_VIEW | CALIBRATE | INFERENCE | EXPORT"
        string target_entity "Participant:PART-001"
        string ip_address
        string details_json
        datetime timestamp
    }

    DATASET_SOURCES {
        uuid id PK
        string source_name "DFUC2020 | DFUC2021 | Medetec | InHouse"
        string license_type
        string dta_number
        string access_restriction
    }
```
