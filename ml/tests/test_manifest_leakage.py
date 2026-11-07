"""
Manifest partition leakage verification tests.
Ensures no patient data is shared between training, validation, and test sets.
"""

import pytest
import pandas as pd
from ml.data.manifests.schema import validate_manifest_dataframe, ManifestValidationError

def test_valid_manifest_zero_leakage():
    df = pd.DataFrame([
        {"image_id": "img1", "participant_code": "PART-001", "wound_code": "W1", "visit_code": "V01", "split": "train"},
        {"image_id": "img2", "participant_code": "PART-001", "wound_code": "W1", "visit_code": "V02", "split": "train"},
        {"image_id": "img3", "participant_code": "PART-002", "wound_code": "W1", "visit_code": "V01", "split": "val"},
        {"image_id": "img4", "participant_code": "PART-003", "wound_code": "W1", "visit_code": "V01", "split": "test"},
    ])

    report = validate_manifest_dataframe(df)
    assert report["status"] == "valid"
    assert report["train_patients"] == 1
    assert report["val_patients"] == 1
    assert report["test_patients"] == 1

def test_patient_leakage_detection():
    # PART-001 appears in both train and test splits (forbidden leakage!)
    df_leaked = pd.DataFrame([
        {"image_id": "img1", "participant_code": "PART-001", "wound_code": "W1", "visit_code": "V01", "split": "train"},
        {"image_id": "img2", "participant_code": "PART-001", "wound_code": "W1", "visit_code": "V02", "split": "test"},
    ])

    with pytest.raises(ManifestValidationError) as exc_info:
        validate_manifest_dataframe(df_leaked)

    assert "Patient leakage detected" in str(exc_info.value)
    assert "PART-001" in str(exc_info.value)
