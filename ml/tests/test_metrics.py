"""
Scientific metric implementation validation tests.
"""

import numpy as np
from ml.evaluation.metrics import (
    compute_dice_score,
    compute_iou_score,
    compute_hd95,
    compute_area_metrics,
    compute_brier_score,
    compute_ece,
)

def test_dice_and_iou_exact_match():
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[20:60, 20:60] = 1

    dice = compute_dice_score(mask, mask)
    iou = compute_iou_score(mask, mask)

    assert abs(dice - 1.0) < 1e-4
    assert abs(iou - 1.0) < 1e-4

def test_dice_and_iou_disjoint():
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.zeros((100, 100), dtype=np.uint8)
    mask1[:30, :30] = 1
    mask2[70:, 70:] = 1

    dice = compute_dice_score(mask1, mask2)
    iou = compute_iou_score(mask1, mask2)

    assert dice < 0.01
    assert iou < 0.01

def test_dice_half_overlap():
    mask1 = np.zeros((100, 100), dtype=np.uint8)
    mask2 = np.zeros((100, 100), dtype=np.uint8)
    # Area = 40x40 = 1600
    mask1[20:60, 20:60] = 1
    # Overlap = 40x20 = 800
    mask2[20:60, 40:80] = 1

    # Dice = 2*800 / (1600 + 1600) = 1600 / 3200 = 0.5
    dice = compute_dice_score(mask1, mask2)
    # IoU = 800 / (1600 + 1600 - 800) = 800 / 2400 = 0.3333
    iou = compute_iou_score(mask1, mask2)

    assert abs(dice - 0.5) < 1e-3
    assert abs(iou - (1.0 / 3.0)) < 1e-3

def test_hd95_metric():
    mask1 = np.zeros((50, 50), dtype=np.uint8)
    mask2 = np.zeros((50, 50), dtype=np.uint8)
    mask1[10:20, 10:20] = 1
    mask2[10:20, 10:20] = 1

    hd95 = compute_hd95(mask1, mask2)
    assert hd95 == 0.0

def test_brier_and_ece():
    probs = np.array([0.9, 0.8, 0.2, 0.1])
    labels = np.array([1, 1, 0, 0])

    brier = compute_brier_score(probs, labels)
    ece = compute_ece(probs, labels)

    assert brier < 0.1
    assert ece < 0.25
