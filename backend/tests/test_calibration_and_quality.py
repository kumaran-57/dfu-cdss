"""
Calibration calculation and image quality check tests.
"""

import io
from PIL import Image as PILImage
from backend.app.services.calibration import (
    calculate_scale_from_manual_points,
    compute_calibrated_area_cm2,
)
from backend.app.services.quality import compute_blur_and_exposure

def test_manual_scale_calibration():
    # 100 pixels representing 10mm
    points = [[50.0, 50.0], [150.0, 50.0]]
    mm_per_px, conf = calculate_scale_from_manual_points(points, known_dimension_mm=10.0)
    assert abs(mm_per_px - 0.1) < 1e-4
    assert conf >= 0.9

def test_calibrated_area_calculation():
    # 10,000 pixels with 0.1 mm/pixel -> 10,000 * 0.01 mm² = 100 mm² = 1.0 cm²
    area_cm2 = compute_calibrated_area_cm2(pixel_area=10000, mm_per_pixel=0.1)
    assert area_cm2 == 1.0

def test_uncalibrated_area_refusal():
    """Confirms that without scale factor, calibrated area is None."""
    area_cm2 = compute_calibrated_area_cm2(pixel_area=10000, mm_per_pixel=None)
    assert area_cm2 is None

def test_blur_and_exposure_assessment(tmp_path):
    img_file = tmp_path / "test_sharp.jpg"
    # Create sharp test image with high contrast grid
    img = PILImage.new("RGB", (200, 200), color=(128, 128, 128))
    for x in range(0, 200, 10):
        for y in range(0, 200, 10):
            img.putpixel((x, y), (255, 255, 255))
    img.save(img_file, "JPEG")

    blur_score, exposure, passed, recs = compute_blur_and_exposure(str(img_file))
    assert blur_score > 40.0
    assert exposure == "normal"
    assert passed is True
