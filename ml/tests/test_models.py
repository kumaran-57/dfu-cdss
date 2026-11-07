"""
Wound segmentation model forward inference tests.
"""

import numpy as np
from ml.models.segmentation.unet import UNetBaseline
from ml.models.segmentation.segformer import SegFormerB0

def test_unet_inference_shape_and_metadata():
    model = UNetBaseline()
    dummy_img = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

    mask, meta = model.predict(dummy_img)

    assert mask.shape == (256, 256)
    assert meta["model"] == "unet_baseline"
    assert "pixel_area" in meta
    assert meta["granulation_percentage"] + meta["slough_percentage"] + meta["necrotic_percentage"] == 100.0

def test_segformer_inference_shape_and_metadata():
    model = SegFormerB0()
    dummy_img = np.random.randint(0, 255, (256, 256, 3), dtype=np.uint8)

    mask, meta = model.predict(dummy_img)

    assert mask.shape == (256, 256)
    assert meta["model"] == "segformer_b0"
    assert "uncertainty_score" in meta
    assert 0.0 <= meta["uncertainty_score"] <= 1.0
