"""
Audit Log Inspection and De-identified Research Export API.
"""

import io
import csv
from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.participant import Participant
from backend.app.models.visit import Visit
from backend.app.models.image import Image
from backend.app.models.prediction import Prediction
from backend.app.models.audit import AuditLog
from backend.app.schemas.audit import AuditLogListResponse
from backend.app.security.auth import get_current_user, RoleChecker
from backend.app.services.audit import log_audit_event

router = APIRouter(tags=["Audit & Research"])

require_admin = RoleChecker(["admin"])
require_researcher_or_admin = RoleChecker(["admin", "researcher", "clinician"])

@router.get("/audit/logs", response_model=AuditLogListResponse)
def list_audit_logs(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    action: Optional[str] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Inspects immutable system audit trail (Admin only)."""
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))

    total = query.count()
    items = query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit).all()

    return {"total": total, "items": items}

@router.get("/research/metrics")
def get_research_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_researcher_or_admin),
):
    """Returns aggregated research study statistics."""
    total_participants = db.query(Participant).count()
    total_visits = db.query(Visit).count()
    total_images = db.query(Image).count()
    total_predictions = db.query(Prediction).count()
    flagged_reviews = db.query(Prediction).filter(Prediction.review_required == True).count()

    return {
        "total_participants": total_participants,
        "total_visits": total_visits,
        "total_images": total_images,
        "total_predictions": total_predictions,
        "flagged_for_clinician_review": flagged_reviews,
        "review_rate_percentage": round((flagged_reviews / max(1, total_predictions)) * 100, 1),
    }

@router.post("/research/exports/csv")
def export_deidentified_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_researcher_or_admin),
):
    """
    Generates de-identified tabular CSV export for research analysis.
    Contains no direct patient identifiers.
    """
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "study_id",
        "biological_sex",
        "age_at_enrollment",
        "visit_code",
        "follow_up_day",
        "wound_side",
        "anatomical_location",
        "calibrated_area_cm2",
        "major_length_mm",
        "minor_width_mm",
        "granulation_percentage",
        "slough_percentage",
        "necrotic_percentage",
        "uncertainty_score",
    ])

    participants = db.query(Participant).all()
    for p in participants:
        visits = db.query(Visit).filter(Visit.participant_id == p.id).all()
        for v in visits:
            images = db.query(Image).filter(Image.visit_id == v.id).all()
            for img in images:
                pred = db.query(Prediction).filter(Prediction.image_id == img.id).first()
                writer.writerow([
                    p.study_id,
                    p.biological_sex,
                    p.age_at_enrollment,
                    v.visit_code,
                    v.follow_up_day,
                    v.wound_side,
                    v.anatomical_location,
                    pred.calibrated_area_cm2 if pred else "",
                    pred.major_length_mm if pred else "",
                    pred.minor_width_mm if pred else "",
                    pred.granulation_percentage if pred else "",
                    pred.slough_percentage if pred else "",
                    pred.necrotic_percentage if pred else "",
                    pred.uncertainty_score if pred else "",
                ])

    log_audit_event(
        db,
        action="RESEARCH_DATA_EXPORTED",
        target_entity="Cohort:AllParticipants",
        user_id=str(current_user.id),
        details={"format": "CSV", "exported_by_role": current_user.role},
    )

    csv_data = output.getvalue()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=dfu_xai_cohort_export.csv"},
    )
