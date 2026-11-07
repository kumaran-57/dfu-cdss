"""
Participant and Consent Management API.
Enforces non-identifying research study IDs and consent verification.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.participant import Participant
from backend.app.schemas.participant import (
    ParticipantCreate,
    ParticipantUpdate,
    ParticipantResponse,
    ParticipantListResponse,
)
from backend.app.security.auth import get_current_user, RoleChecker
from backend.app.services.audit import log_audit_event

router = APIRouter(prefix="/participants", tags=["Participants"])

require_write_access = RoleChecker(["admin", "clinician"])

@router.get("", response_model=ParticipantListResponse)
def list_participants(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    study_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves paginated list of research participants."""
    query = db.query(Participant)
    if study_id:
        query = query.filter(Participant.study_id.ilike(f"%{study_id}%"))

    total = query.count()
    items = query.order_by(Participant.created_at.desc()).offset(skip).limit(limit).all()

    return {"total": total, "items": items}

@router.post("", response_model=ParticipantResponse, status_code=status.HTTP_201_CREATED)
def create_participant(
    body: ParticipantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_write_access),
):
    """Registers a coded research participant (Clinician or Admin only)."""
    existing = db.query(Participant).filter(Participant.study_id == body.study_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Participant with Study ID '{body.study_id}' already registered",
        )

    participant = Participant(
        study_id=body.study_id,
        biological_sex=body.biological_sex,
        age_at_enrollment=body.age_at_enrollment,
        enrollment_status=body.enrollment_status,
        consent_version=body.consent_version,
        consent_status="granted",
    )
    db.add(participant)
    db.commit()
    db.refresh(participant)

    log_audit_event(
        db,
        action="PARTICIPANT_REGISTERED",
        target_entity=f"Participant:{participant.study_id}",
        user_id=str(current_user.id),
        details={"consent_version": participant.consent_version},
    )

    return participant

@router.get("/{id}", response_model=ParticipantResponse)
def get_participant(
    id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves a single participant by UUID."""
    p = db.query(Participant).filter(Participant.id == id).first()
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found",
        )
    return p

@router.put("/{id}", response_model=ParticipantResponse)
def update_participant(
    id: str,
    body: ParticipantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_write_access),
):
    """Updates participant demographics or consent status."""
    p = db.query(Participant).filter(Participant.id == id).first()
    if not p:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found",
        )

    if body.biological_sex is not None:
        p.biological_sex = body.biological_sex
    if body.age_at_enrollment is not None:
        p.age_at_enrollment = body.age_at_enrollment
    if body.enrollment_status is not None:
        p.enrollment_status = body.enrollment_status
    if body.consent_status is not None:
        p.consent_status = body.consent_status

    db.commit()
    db.refresh(p)

    log_audit_event(
        db,
        action="PARTICIPANT_UPDATED",
        target_entity=f"Participant:{p.study_id}",
        user_id=str(current_user.id),
        details={"consent_status": p.consent_status},
    )

    return p
