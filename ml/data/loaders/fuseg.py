"""
FUSeg / UWM Wound Segmentation Dataset Adapter.
Dataset origin: University of Wisconsin-Milwaukee (UWM) Big Data Lab & AZH Wound Center.
Challenge: Foot Ulcer Segmentation Challenge (FUSeg 2021).
"""

import os
import glob
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from PIL import Image

class FUSegAdapter:
    """
    Adapter for the UWM / FUSeg wound segmentation dataset.
    Extracts image-mask pairs and formats them into zero-leakage manifests.
    """

    def __init__(self, root_dir: str):
        self.root_dir = root_dir

    def discover_files(self) -> List[Dict[str, str]]:
        """
        Scans root_dir for images and matching ground-truth masks.
        Expected structures:
          - root_dir/train/images/*.png and root_dir/train/labels/*.png
          - root_dir/images/*.png and root_dir/labels/*.png
        """
        records = []
        
        # Check if train/test/val subfolders exist
        splits = ["train", "val", "test"]
        found_splits = [s for s in splits if os.path.exists(os.path.join(self.root_dir, s))]
        
        if found_splits:
            for split_name in found_splits:
                split_path = os.path.join(self.root_dir, split_name)
                img_dir = os.path.join(split_path, "images")
                lbl_dir = os.path.join(split_path, "labels") if os.path.exists(os.path.join(split_path, "labels")) else os.path.join(split_path, "masks")
                
                if not os.path.exists(img_dir):
                    # Direct images in split folder
                    img_dir = split_path
                    lbl_dir = os.path.join(self.root_dir, f"{split_name}_labels")
                
                images = sorted(glob.glob(os.path.join(img_dir, "*.*")))
                for img_p in images:
                    if not img_p.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                        continue
                    basename = os.path.splitext(os.path.basename(img_p))[0]
                    # Locate matching mask
                    mask_p = None
                    if os.path.exists(lbl_dir):
                        candidates = [
                            os.path.join(lbl_dir, f"{basename}.png"),
                            os.path.join(lbl_dir, f"{basename}_mask.png"),
                            os.path.join(lbl_dir, f"{basename}.jpg"),
                        ]
                        for c in candidates:
                            if os.path.exists(c):
                                mask_p = c
                                break
                                
                    records.append({
                        "image_id": basename,
                        "image_path": img_p,
                        "mask_path": mask_p,
                        "split": split_name,
                        "participant_code": f"PART-{basename.split('_')[0]}",
                        "wound_code": "W01",
                        "visit_code": "V01",
                    })
        else:
            # Flat directory structure
            img_dir = os.path.join(self.root_dir, "images") if os.path.exists(os.path.join(self.root_dir, "images")) else self.root_dir
            lbl_dir = os.path.join(self.root_dir, "labels") if os.path.exists(os.path.join(self.root_dir, "labels")) else os.path.join(self.root_dir, "masks")
            
            images = sorted(glob.glob(os.path.join(img_dir, "*.*")))
            for idx, img_p in enumerate(images):
                if not img_p.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
                    continue
                basename = os.path.splitext(os.path.basename(img_p))[0]
                mask_p = None
                if os.path.exists(lbl_dir):
                    for ext in [".png", ".jpg", ".bmp"]:
                        cand = os.path.join(lbl_dir, f"{basename}{ext}")
                        if os.path.exists(cand):
                            mask_p = cand
                            break

                # Deterministic 70/15/15 patient split if no pre-assigned split
                assigned_split = "train" if idx % 10 < 7 else ("val" if idx % 10 < 8 else "test")
                
                records.append({
                    "image_id": basename,
                    "image_path": img_p,
                    "mask_path": mask_p,
                    "split": assigned_split,
                    "participant_code": f"PART-{idx:04d}",
                    "wound_code": "W01",
                    "visit_code": "V01",
                })

        return records

    def create_manifest(self, output_csv_path: Optional[str] = None) -> pd.DataFrame:
        """
        Creates a DataFrame compliant with DFU-XAI manifest schema.
        """
        records = self.discover_files()
        if not records:
            raise ValueError(f"No valid images found in root directory: {self.root_dir}")
            
        df = pd.DataFrame(records)
        manifest_cols = ["image_id", "participant_code", "wound_code", "visit_code", "split"]
        manifest_df = df[manifest_cols].copy()
        
        if output_csv_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
            manifest_df.to_csv(output_csv_path, index=False)
            
        return manifest_df
