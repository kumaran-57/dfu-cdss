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

def test_fuseg_adapter_manifest_generation(tmp_path):
    from ml.data.loaders.fuseg import FUSegAdapter
    
    # Create mock FUSeg directory structure
    train_imgs = tmp_path / "train" / "images"
    train_lbls = tmp_path / "train" / "labels"
    train_imgs.mkdir(parents=True)
    train_lbls.mkdir(parents=True)
    
    (train_imgs / "0001.png").write_text("mock_img")
    (train_lbls / "0001.png").write_text("mock_mask")
    (train_imgs / "0002.png").write_text("mock_img")
    (train_lbls / "0002.png").write_text("mock_mask")
    
    val_imgs = tmp_path / "val" / "images"
    val_lbls = tmp_path / "val" / "labels"
    val_imgs.mkdir(parents=True)
    val_lbls.mkdir(parents=True)
    (val_imgs / "0003.png").write_text("mock_img")
    (val_lbls / "0003.png").write_text("mock_mask")
    
    adapter = FUSegAdapter(root_dir=str(tmp_path))
    manifest_df = adapter.create_manifest()
    
    assert len(manifest_df) == 3
    report = validate_manifest_dataframe(manifest_df)
    assert report["status"] == "valid"
    assert report["train_images"] == 2
    assert report["val_images"] == 1

