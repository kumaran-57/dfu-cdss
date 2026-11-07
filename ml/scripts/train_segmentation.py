#!/usr/bin/env python3
"""
Segmentation Model Training Script (SegFormer-B0 and U-Net).
Usage:
    python -m ml.scripts.train_segmentation --config experiments/configs/e2_segmentation.yaml --manifest path/to/manifest.csv
"""

import sys
import os
import argparse
import yaml
import numpy as np
from ml.data.manifests.schema import validate_manifest_file, ManifestValidationError
from ml.models.segmentation.unet import UNetBaseline
from ml.models.segmentation.segformer import SegFormerB0

def main():
    parser = argparse.ArgumentParser(description="Train wound segmentation models")
    parser.add_argument("--config", default="experiments/configs/e2_segmentation.yaml", help="Path to experiment config YAML")
    parser.add_argument("--manifest", default=None, help="Path to validated dataset manifest CSV")
    parser.add_argument("--epochs", type=int, default=10, help="Number of training epochs")
    parser.add_argument("--model", choices=["unet", "segformer"], default="segformer", help="Model architecture")
    args = parser.parse_args()

    print("=" * 60)
    print("DFU-XAI Wound Segmentation Training Runner")
    print("=" * 60)

    # 1. Check Manifest & Real Data Status
    if not args.manifest or not os.path.exists(args.manifest):
        print("\n[BLOCKED: DATASET ACCESS]")
        print("  Real clinical datasets (e.g. DFUC2020 / DFUC2021) are not present in the workspace.")
        print("  In accordance with Research Ethics rules (Section 2.2 & 2.3):")
        print("    - Training on real patient data is held pending signed Data Transfer Agreements (DTA).")
        print("    - No fabricated patient images or fake accuracy metrics will be generated.")
        print("\n  To train when you have received approved dataset access:")
        print("    1. Place images in an external directory outside Git.")
        print("    2. Generate manifest CSV with columns: image_id, participant_code, wound_code, visit_code, split")
        print("    3. Validate manifest: python -m ml.scripts.validate_manifest --manifest your_manifest.csv")
        print("    4. Run training: python -m ml.scripts.train_segmentation --manifest your_manifest.csv")
        print("=" * 60)
        sys.exit(0)

    # If manifest is supplied, validate partition isolation first
    try:
        report = validate_manifest_file(args.manifest)
        print(f"✓ Manifest validated: {report['total_images']} images across {report['total_participants']} patients.")
    except ManifestValidationError as e:
        print(f"✗ Manifest Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"\nInitializing {args.model.upper()} training pipeline for {args.epochs} epochs...")
    print("Device: CPU execution mode")
    print("Starting training loop...")

if __name__ == "__main__":
    main()
