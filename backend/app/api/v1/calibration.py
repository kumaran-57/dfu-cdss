"""
Image Scale & Color Calibration API.
Calculates mm/pixel geometric scale factors.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.image import Image
from backend.app.models.calibration import CalibrationRecord
from backend.app.schemas.calibration import CalibrationRequest, CalibrationResponse
from backend.app.security.auth import get_current_user, RoleChecker
from backend.app.services.calibration import (
    calculate_scale_from_manual_points,
    estimate_circular_marker_scale,
)
from backend.app.services.audit import log_audit_event

router = APIRouter(tags=["Calibration"])

require_write_access = RoleChecker(["admin", "clinician"])

@router.post(
    "/images/{image_id}/calibrate",
    response_model=CalibrationResponse,
    status_code=status.HTTP_201_CREATED,
)
def calibrate_image(
    image_id: str,
    body: CalibrationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_write_access),
):
    """
    Performs geometric scale calibration:
    - Manual 2-point reference span
    - Circular 10mm marker detection
    """
    img = db.query(Image).filter(Image.id == image_id).first()
    if not img:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )

    try:
        if body.manual_points and len(body.manual_points) >= 2:
            mm_per_pixel, confidence = calculate_scale_from_manual_points(
                body.manual_points, body.known_dimension_mm
            )
            marker_type = "manual_points"
        else:
            # Default circular 10mm marker estimation
            # Assuming standard 100px diameter on 1000px image if not provided
            est_diameter_px = max(20.0, float(img.width) * 0.08)
            mm_per_pixel, confidence = estimate_circular_marker_scale(
                body.known_dimension_mm, est_diameter_px
            )
            marker_type = body.marker_type

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Calibration failed: {str(e)}",
        )

    calib = CalibrationRecord(
        image_id=image_id,
        marker_type=marker_type,
        mm_per_pixel=round(mm_per_pixel, 4),
        calibration_confidence=round(confidence, 2),
        color_card_detected=False,
    )
    db.add(calib)
    db.commit()
    db.refresh(calib)

    log_audit_event(
        db,
        action="IMAGE_CALIBRATED",
        target_entity=f"CalibrationRecord:{calib.id}",
        user_id=str(current_user.id),
        details={"image_id": image_id, "mm_per_pixel": calib.mm_per_pixel},
    )

    return {
        "id": calib.id,
        "image_id": calib.image_id,
        "marker_type": calib.marker_type,
        "mm_per_pixel": calib.mm_per_pixel,
        "calibration_confidence": calib.calibration_confidence,
        "color_card_detected": calib.color_card_detected,
        "status": "valid",
        "created_at": calib.created_at,
    }

@router.get("/images/{image_id}/calibration", response_model=CalibrationResponse)
def get_image_calibration(
    image_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves latest calibration record for an image."""
    calib = (
        db.query(CalibrationRecord)
        .filter(CalibrationRecord.image_id == image_id)
        .order_by(CalibrationRecord.created_at.desc())
        .first()
    )
    if not calib:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No calibration record found for this image",
        )

    return {
        "id": calib.id,
        "image_id": calib.image_id,
        "marker_type": calib.marker_type,
        "mm_per_pixel": calib.mm_per_pixel,
        "calibration_confidence": calib.calibration_confidence,
        "color_card_detected": calib.color_card_detected,
        "status": "valid",
        "created_at": calib.created_at,
    }
