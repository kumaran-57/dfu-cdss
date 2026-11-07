"""
Dataset Manifest Schema and Partition Leakage Validation.
Guarantees patient-level data partitioning across train, validation, and test splits.
"""

from typing import List, Dict, Any, Set
import pandas as pd

REQUIRED_COLUMNS = [
    "image_id",
    "participant_code",
    "wound_code",
    "visit_code",
    "split",  # 'train', 'val', 'test'
]

VALID_SPLITS = {"train", "val", "test"}

class ManifestValidationError(Exception):
    pass

def validate_manifest_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Validates manifest integrity and guarantees patient-level partition isolation.
    """
    # 1. Check required headers
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ManifestValidationError(f"Missing required columns in manifest: {missing_cols}")

    # 2. Check valid split labels
    invalid_splits = set(df["split"].unique()) - VALID_SPLITS
    if invalid_splits:
        raise ManifestValidationError(f"Invalid split values found: {invalid_splits}. Must be train/val/test.")

    # 3. CRITICAL: Check zero patient-level overlap across splits
    train_patients: Set[str] = set(df[df["split"] == "train"]["participant_code"].dropna())
    val_patients: Set[str] = set(df[df["split"] == "val"]["participant_code"].dropna())
    test_patients: Set[str] = set(df[df["split"] == "test"]["participant_code"].dropna())

    train_val_leakage = train_patients.intersection(val_patients)
    train_test_leakage = train_patients.intersection(test_patients)
    val_test_leakage = val_patients.intersection(test_patients)

    if train_val_leakage or train_test_leakage or val_test_leakage:
        raise ManifestValidationError(
            f"Patient leakage detected! "
            f"Train/Val overlap: {train_val_leakage}, "
            f"Train/Test overlap: {train_test_leakage}, "
            f"Val/Test overlap: {val_test_leakage}"
        )

    return {
        "status": "valid",
        "total_images": len(df),
        "total_participants": len(df["participant_code"].unique()),
        "train_images": len(df[df["split"] == "train"]),
        "val_images": len(df[df["split"] == "val"]),
        "test_images": len(df[df["split"] == "test"]),
        "train_patients": len(train_patients),
        "val_patients": len(val_patients),
        "test_patients": len(test_patients),
    }

def validate_manifest_file(file_path: str) -> Dict[str, Any]:
    df = pd.read_csv(file_path)
    return validate_manifest_dataframe(df)
