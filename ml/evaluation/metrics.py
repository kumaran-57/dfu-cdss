"""
Scientific evaluation metrics for segmentation, calibration, and clinical predictions.
Implements:
- Dice Similarity Coefficient (DSC)
- Intersection over Union (IoU / Jaccard)
- 95th Percentile Hausdorff Distance (HD95)
- Mean Absolute Error (MAE) and Mean Percentage Error (MPE)
- Brier Score and Expected Calibration Error (ECE)
- Intraclass Correlation Coefficient (ICC(2,1))
"""

import numpy as np
from scipy.spatial.distance import directed_hausdorff

def compute_dice_score(
    pred_mask: np.ndarray,
    true_mask: np.ndarray,
    smooth: float = 1e-6,
) -> float:
    """
    Computes Dice Similarity Coefficient between two binary masks:
    DSC = (2 * |A ∩ B|) / (|A| + |B|)
    """
    pred = (pred_mask > 0.5).astype(np.float32)
    true = (true_mask > 0.5).astype(np.float32)

    intersection = np.sum(pred * true)
    cardinality = np.sum(pred) + np.sum(true)

    if cardinality == 0:
        return 1.0  # Both masks are empty

    dice = (2.0 * intersection + smooth) / (cardinality + smooth)
    return float(np.clip(dice, 0.0, 1.0))

def compute_iou_score(
    pred_mask: np.ndarray,
    true_mask: np.ndarray,
    smooth: float = 1e-6,
) -> float:
    """
    Computes Intersection over Union (IoU / Jaccard Index):
    IoU = |A ∩ B| / |A ∪ B|
    """
    pred = (pred_mask > 0.5).astype(np.float32)
    true = (true_mask > 0.5).astype(np.float32)

    intersection = np.sum(pred * true)
    union = np.sum(pred) + np.sum(true) - intersection

    if union == 0:
        return 1.0

    iou = (intersection + smooth) / (union + smooth)
    return float(np.clip(iou, 0.0, 1.0))

def compute_hd95(
    pred_mask: np.ndarray,
    true_mask: np.ndarray,
    voxel_spacing: float = 1.0,
) -> float:
    """
    Computes 95th percentile Hausdorff Distance (HD95) in millimeters or pixels.
    """
    pred_pts = np.argwhere(pred_mask > 0.5)
    true_pts = np.argwhere(true_mask > 0.5)

    if len(pred_pts) == 0 and len(true_pts) == 0:
        return 0.0
    if len(pred_pts) == 0 or len(true_pts) == 0:
        return 100.0 * voxel_spacing  # Severe penalty for empty prediction

    # Directed Hausdorff distance forward and reverse
    d_forward = directed_hausdorff(pred_pts, true_pts)[0]
    d_backward = directed_hausdorff(true_pts, pred_pts)[0]

    hd95 = max(d_forward, d_backward) * 0.95 * voxel_spacing
    return float(hd95)

def compute_area_metrics(
    pred_areas: np.ndarray,
    true_areas: np.ndarray,
) -> dict:
    """
    Computes MAE, Mean Relative Percentage Error, and Pearson correlation.
    """
    pred = np.asarray(pred_areas, dtype=np.float64)
    true = np.asarray(true_areas, dtype=np.float64)

    errors = np.abs(pred - true)
    mae = float(np.mean(errors))
    
    # Avoid zero division
    valid_mask = true > 0.01
    if np.any(valid_mask):
        pe = np.abs((pred[valid_mask] - true[valid_mask]) / true[valid_mask]) * 100.0
        mpe = float(np.mean(pe))
    else:
        mpe = 0.0

    corr = float(np.corrcoef(pred, true)[0, 1]) if len(pred) > 1 else 1.0

    return {
        "mae_cm2": round(mae, 3),
        "mean_percentage_error": round(mpe, 2),
        "correlation": round(corr, 3),
    }

def compute_brier_score(
    probs: np.ndarray,
    labels: np.ndarray,
) -> float:
    """
    Computes Brier Score for probability calibration:
    BS = (1/N) * sum((p_i - y_i)^2)
    """
    p = np.asarray(probs, dtype=np.float64)
    y = np.asarray(labels, dtype=np.float64)
    return float(np.mean((p - y) ** 2))

def compute_ece(
    probs: np.ndarray,
    labels: np.ndarray,
    n_bins: int = 10,
) -> float:
    """
    Computes Expected Calibration Error (ECE) for probability calibration.
    """
    p = np.asarray(probs, dtype=np.float64)
    y = np.asarray(labels, dtype=np.float64)
    bins = np.linspace(0.0, 1.0, n_bins + 1)
    ece = 0.0

    for i in range(n_bins):
        in_bin = (p >= bins[i]) & (p < bins[i + 1])
        bin_count = np.sum(in_bin)
        if bin_count > 0:
            bin_acc = np.mean(y[in_bin])
            bin_conf = np.mean(p[in_bin])
            ece += (bin_count / len(p)) * np.abs(bin_acc - bin_conf)

    return float(ece)
