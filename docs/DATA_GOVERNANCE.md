# Data Governance & Privacy Architecture

This document governs the processing, retention, de-identification, and export of research data within the DFU-XAI platform.

---

## 1. Ethical Foundation & Principles

1. **Principle of Non-Identification**: Direct identifiers (names, government IDs, phone numbers, hospital MRNs, faces, tattoos, wristbands) must never enter the research repository.
2. **Informed Consent**: Every participant record must be paired with an active, validated consent entry (`docs/ETHICS_AND_CONSENT_CHECKLIST.md`).
3. **Role-Based Least Privilege**:
   - `admin`: User provisioning and system audit logs only; no arbitrary export of unblinded study data.
   - `clinician`: Access to active patients and visit management; review and override AI predictions.
   - `researcher`: Read-only access to coded, de-identified research cohorts and experiment evaluation metrics.
   - `viewer`: Read-only demonstration / review access.

---

## 2. Ingestion & Preprocessing Security Controls

- **EXIF Stripping**: All uploaded photographic assets are stripped of EXIF tags (GPS coordinates, camera serial numbers, capture timestamps, device owner strings) prior to persisting in the object store.
- **Hash Integrity**: Each image record computes a SHA-256 digest at ingestion to verify image immutability and prevent silent file tampering.
- **Upload Restrictions**: Strict MIME-type sniffing (`image/jpeg`, `image/png`) and file-size quotas (maximum 25MB).

---

## 3. Data Retention & Revocation

- **Right to Withdraw**: If a participant withdraws consent, their study record status transitions to `withdrawn`. Associated images and raw records are archived to an encrypted, read-isolated retention vault in compliance with research ethics board retention guidelines.
- **Audit Trail**: Every access event (read, update, export, login) is cryptographically timestamped and immutably recorded in the `audit_logs` table.
