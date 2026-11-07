# DFU-XAI Data Dictionary

This document defines variables, units, valid ranges, and allowed categories for structured data in the DFU-XAI framework.

---

## 1. Participant Entity

| Field | Type | Units / Format | Allowed Values / Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `study_id` | String | `PART-[0-9]{3,5}` | Unique, non-identifying | Research participant identifier. |
| `biological_sex` | String | Categorical | `female`, `male`, `other`, `undisclosed` | Biological sex at birth for statistical normalization. |
| `age_at_enrollment` | Integer | Years | $18 \le \text{age} \le 110$ | Age at baseline visit. |
| `enrollment_status` | String | Categorical | `active`, `completed`, `withdrawn`, `lost_to_followup` | Study status. |

---

## 2. Clinical Observation Entity

| Field | Type | Units | Valid Range | Source Requirement | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `hba1c_percentage` | Float | $\%$ (DCCT) | $4.0 - 18.0$ | Lab report / POC assay | Glycated hemoglobin. |
| `neuropathy_present` | Boolean | Binary | `true` (sensory loss $\ge 1$ site), `false` | 10g Semmes-Weinstein monofilament test | Diabetic peripheral neuropathy. |
| `abi_index` | Float | Ratio | $0.2 - 2.5$ | Doppler ultrasound test | Ankle-brachial index ($<0.9$ indicates PAD). |
| `infection_status` | String | Categorical | `none`, `superficial`, `deep`, `systemic_sepsis` | Clinician examination | IWGDF / IDSA infection classification. |
| `offloading_modality` | String | Categorical | `none`, `total_contact_cast`, `removable_cast_walker`, `therapeutic_footwear` | Clinician prescription | Pressure offloading strategy. |

---

## 3. Image & Calibration Entity

| Field | Type | Units | Valid Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `blur_score` | Float | Laplacian variance | $\ge 0.0$ ($< 50.0$ flagged as blurry) | Sharpness metric computed via second derivative filter. |
| `exposure_status` | String | Categorical | `normal`, `underexposed`, `overexposed` | Mean RGB luminance inspection ($L < 40$ or $L > 220$). |
| `mm_per_pixel` | Float | $mm / px$ | $0.01 - 2.00$ | Calibrated spatial scale factor. |
| `calibration_confidence` | Float | $[0.0, 1.0]$ | $0.0 - 1.0$ | Confidence score based on marker circularity and edge clarity. |

---

## 4. Wound Prediction Entity

| Field | Type | Units | Valid Range | Description |
| :--- | :--- | :--- | :--- | :--- |
| `calibrated_area_cm2` | Float | $cm^2$ | $\ge 0.0$ (null if uncalibrated) | Calibrated 2D ulcer boundary surface area. |
| `major_length_mm` | Float | $mm$ | $\ge 0.0$ | Maximum Feret diameter (longest distance between boundary points). |
| `minor_width_mm` | Float | $mm$ | $\ge 0.0$ | Maximum perpendicular caliper dimension. |
| `granulation_percentage` | Float | $\%$ | $0.0 - 100.0$ | Proportion of healthy vascularized red tissue. |
| `slough_percentage` | Float | $\%$ | $0.0 - 100.0$ | Proportion of non-viable yellow/fibrinous tissue. |
| `necrotic_percentage` | Float | $\%$ | $0.0 - 100.0$ | Proportion of devitalized black eschar tissue. |
| `uncertainty_score` | Float | Normalized entropy | $[0.0, 1.0]$ ($> 0.35$ triggers review) | Epistemic uncertainty derived from MC Dropout ensemble. |
