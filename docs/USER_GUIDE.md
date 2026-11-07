# DFU-XAI Clinician & Researcher User Guide

## 1. Clinician Workflow

1. **Sign In**: Log into the web portal with clinician credentials. Note the prominent clinical safety disclaimer.
2. **Select or Register Participant**: Select an existing participant via non-identifying Study ID (`PART-XXX`) or register a newly consented patient.
3. **Capture / Ingest Image**:
   - Access the visit capture screen.
   - Position the smartphone camera perpendicular to the ulcer.
   - Ensure the circular reference marker is placed on the skin plane adjacent to the wound.
   - The automated pre-check will reject blurry or severely over/underexposed captures and prompt for recapture.
4. **Inspect AI Assessment**:
   - Inspect the segmented wound boundary overlay and tissue breakdown.
   - Review the calculated area ($cm^2$) and epistemic uncertainty score.
   - If the uncertainty flag indicates high variability, carefully inspect the borders.
5. **Clinician Review & Sign-Off**:
   - Enter clinical notes, approve the measurement or adjust the manual boundary override.
   - Submit the verified review.

---

## 2. Researcher Workflow

1. **Benchmark Access**: Access the Research console to view model comparison leaderboards across E1–E10.
2. **De-Identified Export**: Request an export of calibrated longitudinal time-series data in tabular CSV format for secondary statistical modeling.
