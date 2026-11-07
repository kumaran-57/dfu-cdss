# Security Threat Model (STRIDE Methodology)

This document formalizes the threat model for the DFU-XAI platform across medical privacy, data integrity, and API boundaries.

---

## Threat Matrix

| STRIDE Category | Potential Vulnerability | Mitigation Strategy Implemented in DFU-XAI |
| :--- | :--- | :--- |
| **Spoofing** | Unauthorized user impersonating a clinician to tamper with review notes. | Argon2 / PBKDF2 password hashing, short-lived JWT session tokens, strict role verification decorators. |
| **Tampering** | Modification of de-identified image files or segmentation mask outputs. | SHA-256 hash digests computed at upload and verified upon retrieval; immutable audit trail. |
| **Repudiation** | Clinician denies overriding or approving an automated area calculation. | Timestamped `ClinicianReview` records linked to clinician user ID, storing exact override reason and delta. |
| **Information Disclosure** | Leakage of Protected Health Information (PHI) via image EXIF tags (e.g. GPS, timestamp, device name). | Automated mandatory EXIF scrub upon upload; exclusion of faces/names; non-identifying `PART-XXX` codes. |
| **Denial of Service** | Uploading massive image files or malicious image bombs (decompression bombs) crashing the server. | Upload file-size limit enforced (25MB limit), MIME type validation, memory-capped PIL decompression safeguards. |
| **Elevation of Privilege** | Normal user invoking `/admin/users` or modifying study participant enrollment. | Server-side role validation (`RoleChecker(["admin"])`) on all administrative API endpoints; never trust client state. |
