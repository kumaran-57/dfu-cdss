"""
Procedural synthetic wound and calibration fixture generator.
Strictly marked with is_synthetic = True for software tests and UI demonstration only.
Never used to claim clinical accuracy.
"""

import os
import math
import numpy as np
from PIL import Image as PILImage, ImageDraw, ImageFont

def generate_synthetic_wound_image(
    output_path: str,
    width: int = 800,
    height: int = 800,
    include_calibration_marker: bool = True,
    blur_degrade: bool = False,
) -> str:
    """
    Renders an explicit synthetic wound phantom with:
    - Background skin tone gradient
    - Circular 10mm reference adhesive marker with crosshairs
    - Multilayer ulcer bed (outer margin, yellow slough core, red granulation rim)
    - Prominent 'SYNTHETIC PHANTOM - NOT REAL PATIENT' watermark
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # 1. Base skin tone background with subtle texture
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    # Pale/olive skin tone range RGB (210, 175, 145) with random gaussian grain
    base_color = np.array([215, 180, 150], dtype=np.float32)
    noise = np.random.normal(0, 4, (height, width, 3))
    skin = np.clip(base_color + noise, 0, 255).astype(np.uint8)
    
    img = PILImage.fromarray(skin)
    draw = ImageDraw.Draw(img)

    # 2. Render Calibration Reference Marker (Top-Right or Left)
    if include_calibration_marker:
        marker_center = (120, 120)
        marker_radius = 45  # 90px diameter
        # White adhesive backing
        draw.ellipse(
            [
                marker_center[0] - marker_radius,
                marker_center[1] - marker_radius,
                marker_center[0] + marker_radius,
                marker_center[1] + marker_radius,
            ],
            fill=(245, 245, 245),
            outline=(40, 40, 40),
            width=2,
        )
        # Inner black reference ring
        draw.ellipse(
            [
                marker_center[0] - marker_radius + 10,
                marker_center[1] - marker_radius + 10,
                marker_center[0] + marker_radius - 10,
                marker_center[1] + marker_radius - 10,
            ],
            fill=(20, 20, 20),
        )
        # Calibration text label
        draw.text((80, 170), "10mm REF", fill=(30, 30, 30))

    # 3. Render Irregular Wound Bed
    center_x, center_y = width // 2, height // 2
    base_radius = 140
    num_points = 36
    poly_points = []
    
    # Generate organic wound margin via harmonic perturbation
    for i in range(num_points):
        angle = (2 * math.pi * i) / num_points
        r_perturb = base_radius + 25 * math.sin(3 * angle) + 15 * math.cos(5 * angle)
        px = center_x + r_perturb * math.cos(angle)
        py = center_y + r_perturb * math.sin(angle)
        poly_points.append((px, py))

    # Outer erythematous margin (subtle reddish halo)
    halo_points = []
    for (px, py) in poly_points:
        vx, vy = px - center_x, py - center_y
        halo_points.append((center_x + vx * 1.15, center_y + vy * 1.15))
    draw.polygon(halo_points, fill=(190, 130, 120))

    # Active granulation tissue rim (deep red)
    draw.polygon(poly_points, fill=(160, 35, 35))

    # Central fibrinous slough island (yellowish/creamy core)
    slough_points = []
    for px, py in poly_points:
        vx, vy = px - center_x, py - center_y
        slough_points.append((center_x + vx * 0.45, center_y + vy * 0.45))
    draw.polygon(slough_points, fill=(210, 195, 125))

    # Necrotic center dot
    necrotic_points = []
    for px, py in poly_points:
        vx, vy = px - center_x, py - center_y
        necrotic_points.append((center_x + vx * 0.15, center_y + vy * 0.15))
    draw.polygon(necrotic_points, fill=(45, 30, 30))

    # 4. Mandatory Clinical Safety Watermark
    watermark_text = "SYNTHETIC PHANTOM - NOT REAL PATIENT DATA - FOR SOFTWARE VERIFICATION ONLY"
    draw.rectangle([0, height - 35, width, height], fill=(0, 0, 0))
    draw.text((15, height - 25), watermark_text, fill=(255, 215, 0))

    if blur_degrade:
        from PIL import ImageFilter
        img = img.filter(ImageFilter.GaussianBlur(radius=8))

    img.save(output_path, "JPEG", quality=92)
    return output_path

if __name__ == "__main__":
    out = "data/sample_synthetic/demo_wound_baseline.jpg"
    generate_synthetic_wound_image(out)
    print(f"Generated synthetic demo fixture at: {out}")
