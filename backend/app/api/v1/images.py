"""
Image Ingestion, Quality Assurance & EXIF Scrubbing API.
"""

import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.visit import Visit
from backend.app.models.image import Image
from backend.app.schemas.image import ImageResponse, ImageQualityCheckResponse
from backend.app.security.auth import get_current_user, RoleChecker
from backend.app.services.storage import secure_save_image
from backend.app.services.quality import compute_blur_and_exposure
from backend.app.services.audit import log_audit_event

router = APIRouter(tags=["Images & Quality Checks"])

require_write_access = RoleChecker(["admin", "clinician"])

@router.post(
    "/visits/{visit_id}/images",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_visit_image(
    visit_id: str,
    file: UploadFile = File(...),
    view_label: str = Form("dorsal_aspect"),
    is_synthetic: bool = Form(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_write_access),
):
    """
    Ingests photographic wound capture:
    1. Validates MIME type and file integrity.
    2. Completely scrubs EXIF tags.
    3. Computes Laplacian blur score and mean exposure status.
    4. Computes SHA-256 content digest and stores securely.
    """
    visit = db.query(Visit).filter(Visit.id == visit_id).first()
    if not visit:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit encounter not found",
        )

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty",
        )

    saved_path, mime_type, width, height, sha256_hash = secure_save_image(
        file_bytes=file_bytes,
        original_filename=file.filename or "upload.jpg",
        visit_id=visit_id,
    )

    # Perform automated image quality assessment
    blur_score, exposure_status, quality_passed, _ = compute_blur_and_exposure(saved_path)

    image_record = Image(
        visit_id=visit_id,
        file_path=saved_path,
        mime_type=mime_type,
        width=width,
        height=height,
        sha256_hash=sha256_hash,
        view_label=view_label,
        quality_passed=quality_passed,
        blur_score=blur_score,
        exposure_status=exposure_status,
        is_synthetic=is_synthetic,
    )
    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    log_audit_event(
        db,
        action="IMAGE_INGESTED",
        target_entity=f"Image:{image_record.id}",
        user_id=str(current_user.id),
        details={
            "visit_id": visit_id,
            "sha256": sha256_hash,
            "quality_passed": quality_passed,
            "is_synthetic": is_synthetic,
        },
    )

    return image_record

@router.get("/visits/{visit_id}/images", response_model=List[ImageResponse])
def list_visit_images(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lists images associated with a visit."""
    return db.query(Image).filter(Image.visit_id == visit_id).all()

@router.get("/images/{image_id}/metadata", response_model=ImageResponse)
def get_image_metadata(
    image_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves metadata and quality scores for an image."""
    img = db.query(Image).filter(Image.id == image_id).first()
    if not img:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image not found",
        )
    return img

@router.get("/images/{image_id}/file")
def get_image_file(
    image_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Returns de-identified sanitized image binary for authorized review."""
    img = db.query(Image).filter(Image.id == image_id).first()
    if not img or not os.path.exists(img.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image file not found on disk",
        )
    return FileResponse(img.file_path, media_type=img.mime_type)

@router.post("/images/{image_id}/quality-check", response_model=ImageQualityCheckResponse)
def check_image_quality(
    image_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Performs real-time blur and exposure quality check."""
    img = db.query(Image).filter(Image.id == image_id).first()
    if not img or not os.path.exists(img.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Image record or file not found",
        )

    blur_score, exposure_status, quality_passed, recs = compute_blur_and_exposure(img.file_path)
    
    # Update image record with latest quality assessment
    img.blur_score = blur_score
    img.exposure_status = exposure_status
    img.quality_passed = quality_passed
    db.commit()

    return {
        "image_id": img.id,
        "quality_passed": quality_passed,
        "blur_score": blur_score,
        "is_blurry": blur_score < 40.0,
        "exposure_status": exposure_status,
        "recommendations": recs,
    }
