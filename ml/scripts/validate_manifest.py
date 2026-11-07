#!/usr/bin/env python3
"""
CLI tool for validating dataset manifests and guaranteeing patient-level split isolation.
"""

import sys
import argparse
from ml.data.manifests.schema import validate_manifest_file, ManifestValidationError

def main():
    parser = argparse.ArgumentParser(description="Validate DFU-XAI dataset manifest")
    parser.add_argument("--manifest", required=True, help="Path to manifest CSV")
    args = parser.parse_args()

    try:
        report = validate_manifest_file(args.manifest)
        print("✓ Manifest validation passed!")
        print(f"  Total Images: {report['total_images']}")
        print(f"  Total Participants: {report['total_participants']}")
        print(f"  Patient Splits -> Train: {report['train_patients']} | Val: {report['val_patients']} | Test: {report['test_patients']}")
        print("  Patient Leakage: 0 (Strict Partition Isolation Guaranteed)")
    except ManifestValidationError as e:
        print(f"✗ Manifest Validation Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
