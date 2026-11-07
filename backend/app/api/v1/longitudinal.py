"""
Longitudinal Progression & Healing Trajectory API.
Aggregates serial patient encounters, metric changes, and clinical notices.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.participant import Participant
from backend.app.models.visit import Visit
from backend.app.models.image import Image
from backend.app.models.prediction import Prediction
from backend.app.schemas.longitudinal import LongitudinalTrajectoryResponse
from backend.app.security.auth import get_current_user
from backend.app.services.longitudinal import analyze_wound_trajectory

router = APIRouter(tags=["Longitudinal Progression"])

@router.get(
    "/participants/{participant_id}/progression",
    response_model=LongitudinalTrajectoryResponse,
)
def get_participant_progression(
    participant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Computes participant longitudinal trajectory across all visits:
    - Baseline vs latest calibrated area
    - Rate of area change per week
    - Healing trend classification
    - Includes mandatory non-autonomous clinical decision-support warning
    """
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found",
        )

    visits = (
        db.query(Visit)
        .filter(Visit.participant_id == participant_id)
        .order_by(Visit.follow_up_day.asc())
        .all()
    )

    visit_records = []
    for v in visits:
        # Find latest prediction for this visit
        images = db.query(Image).filter(Image.visit_id == v.id).all()
        img_ids = [img.id for img in images]
        
        pred = None
        if img_ids:
            pred = (
                db.query(Prediction)
                .filter(Prediction.image_id.in_(img_ids))
                .order_by(Prediction.created_at.desc())
                .first()
            )

        review_status = "unassessed"
        if pred:
            review_status = "pending_review" if pred.review_required else "approved"

        visit_records.append({
            "visit_id": v.id,
            "visit_code": v.visit_code,
            "visit_date": v.visit_date,
            "follow_up_day": v.follow_up_day,
            "calibrated_area_cm2": pred.calibrated_area_cm2 if pred else None,
            "granulation_percentage": pred.granulation_percentage if pred else None,
            "slough_percentage": pred.slough_percentage if pred else None,
            "necrotic_percentage": pred.necrotic_percentage if pred else None,
            "uncertainty_score": pred.uncertainty_score if pred else None,
            "review_status": review_status,
        })

    analysis = analyze_wound_trajectory(visit_records)

    return {
        "participant_id": participant.id,
        "study_id": participant.study_id,
        "baseline_area_cm2": analysis["baseline_area_cm2"],
        "latest_area_cm2": analysis["latest_area_cm2"],
        "total_area_change_percentage": analysis["total_area_change_percentage"],
        "healing_trajectory_trend": analysis["healing_trajectory_trend"],
        "healing_rate_cm2_per_week": analysis["healing_rate_cm2_per_week"],
        "points": analysis["points"],
        "clinical_notice": analysis["clinical_notice"],
    }
