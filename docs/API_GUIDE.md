# DFU-XAI REST API Reference Guide

All endpoints are versioned under `/api/v1` and enforce HTTP Bearer JWT authentication unless marked public.

---

## 1. Authentication Endpoints

### `POST /api/v1/auth/login`
- **Access**: Public
- **Request**: Form data with `username` (email) and `password`.
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOi...",
    "token_type": "bearer",
    "role": "clinician",
    "user_id": "8d3e...-...."
  }
  ```

### `GET /api/v1/auth/me`
- **Access**: Authenticated
- **Response**: Current user profile and assigned role.

---

## 2. Participant & Visit Management

### `GET /api/v1/participants`
- **Access**: `clinician`, `researcher`, `admin`
- **Response**: List of de-identified study participants.

### `POST /api/v1/participants`
- **Access**: `clinician`, `admin`
- **Payload**:
  ```json
  {
    "study_id": "PART-001",
    "biological_sex": "male",
    "age_at_enrollment": 64
  }
  ```

### `POST /api/v1/participants/{id}/visits`
- **Access**: `clinician`, `admin`
- **Payload**: `visit_code`, `visit_date`, clinical findings.

---

## 3. Imaging, Calibration & AI Assessment

### `POST /api/v1/visits/{visit_id}/images`
- **Access**: `clinician`
- **Payload**: Multipart file upload. Strips EXIF, checks blur & exposure.

### `POST /api/v1/images/{image_id}/calibrate`
- **Access**: `clinician`, `researcher`
- **Payload**: Marker specification (circle $10\text{ mm}$ or manual pixel coordinates).
- **Response**: $mm/\text{pixel}$ scale factor, confidence, quality flags.

### `POST /api/v1/images/{image_id}/segment`
- **Access**: `clinician`, `researcher`
- **Response**: Wound mask URL, calibrated area ($cm^2$), length, width, tissue composition percentages, and epistemic uncertainty score.

### `POST /api/v1/predictions/{id}/clinician-review`
- **Access**: `clinician`
- **Payload**: Approval status, override area measurement, justification notes.
