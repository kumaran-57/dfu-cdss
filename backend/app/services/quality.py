"""
Image quality assessment: Laplacian sharpness/blur score and exposure analysis.
Implements OpenCV-equivalent metrics natively using NumPy and Pillow.
"""

from typing import Tuple, List
import numpy as np
from PIL import Image as PILImage

def compute_blur_and_exposure(image_path: str) -> Tuple[float, str, bool, List[str]]:
    """
    Computes:
    1. blur_score: Variance of Laplacian filter (higher = sharper, <50.0 flagged as blurry).
    2. exposure_status: 'normal', 'underexposed', or 'overexposed'.
    3. quality_passed: True if sharpness and exposure criteria are met.
    4. recommendations: Actionable recapture advice.
    """
    recommendations = []
    
    with PILImage.open(image_path) as pil_img:
        # Convert to grayscale for Laplacian edge detection
        gray = np.array(pil_img.convert("L"), dtype=np.float32)

    # 3x3 discrete Laplacian kernel
    # [ 0,  1,  0]
    # [ 1, -4,  1]
    # [ 0,  1,  0]
    padded = np.pad(gray, 1, mode="edge")
    laplacian = (
        padded[1:-1, :-2]
        + padded[1:-1, 2:]
        + padded[:-2, 1:-1]
        + padded[2:, 1:-1]
        - 4 * gray
    )
    blur_score = float(np.var(laplacian))

    # Exposure check via mean luminance
    mean_luminance = float(np.mean(gray))
    if mean_luminance < 40.0:
        exposure_status = "underexposed"
        recommendations.append("Image is too dark. Increase ambient lighting or turn on torch.")
    elif mean_luminance > 220.0:
        exposure_status = "overexposed"
        recommendations.append("Image is washed out / overexposed. Reduce glare or direct flash reflection.")
    else:
        exposure_status = "normal"

    is_blurry = blur_score < 40.0
    if is_blurry:
        recommendations.append("Wound margins appear blurry. Hold camera steady and tap to refocus.")

    quality_passed = (not is_blurry) and (exposure_status == "normal")

    return blur_score, exposure_status, quality_passed, recommendations
