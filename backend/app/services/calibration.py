"""
Planar scale calibration service.
Computes scale factor (mm/pixel) and calibrated metric dimensions.
"""

import math
from typing import Optional, List, Tuple

def calculate_scale_from_manual_points(
    points: List[List[float]],
    known_dimension_mm: float = 10.0,
) -> Tuple[float, float]:
    """
    Computes mm_per_pixel from two calibration points: [[x1, y1], [x2, y2]].
    Returns: (mm_per_pixel, confidence)
    """
    if len(points) < 2:
        raise ValueError("At least 2 points are required for scale calibration")

    p1, p2 = points[0], points[1]
    pixel_distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
    
    if pixel_distance < 5.0:
        raise ValueError("Reference marker span is too small (<5 pixels) for reliable calibration")

    mm_per_pixel = known_dimension_mm / pixel_distance
    confidence = 0.95  # Manual point confirmation by clinician

    return float(mm_per_pixel), float(confidence)

def estimate_circular_marker_scale(
    known_diameter_mm: float = 10.0,
    estimated_diameter_pixels: float = 100.0,
) -> Tuple[float, float]:
    """
    Standard circular reference calibration (e.g. 10mm adhesive dot).
    """
    if estimated_diameter_pixels <= 0:
        raise ValueError("Estimated marker diameter must be positive")
    
    mm_per_pixel = known_diameter_mm / estimated_diameter_pixels
    confidence = 0.90
    return float(mm_per_pixel), float(confidence)

def compute_calibrated_area_cm2(
    pixel_area: int,
    mm_per_pixel: Optional[float],
) -> Optional[float]:
    """
    Converts pixel area to metric square centimeters (cm²).
    Returns None if uncalibrated.
    """
    if mm_per_pixel is None or mm_per_pixel <= 0:
        return None
    # 1 pixel = (mm_per_pixel)^2 mm^2
    # 1 cm^2 = 100 mm^2
    area_mm2 = float(pixel_area) * (mm_per_pixel ** 2)
    area_cm2 = area_mm2 / 100.0
    return round(area_cm2, 3)
