"""
Visit and Clinical Observation API.
Manages longitudinal encounters, clinical biomarkers, and offloading metadata.
"""

from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.models.participant import Participant
from backend.app.models.visit import Visit
from backend.app.models.clinical import ClinicalObservation
from backend.app.schemas.visit import VisitCreate, VisitResponse, VisitListResponse
from backend.app.schemas.clinical import (
    ClinicalObservationCreate,
    ClinicalObservationResponse,
)
from backend.app.security.auth import get_current_user, RoleChecker
from backend.app.services.audit import log_audit_event

router = APIRouter(tags=["Visits & Observations"])

require_write_access = RoleChecker(["admin", "clinician"])

@router.get(
    "/participants/{participant_id}/visits",
    response_model=VisitListResponse,
)
def list_participant_visits(
    participant_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lists all consultation visits for a research participant."""
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
    return {"total": len(visits), "items": visits}

@router.post(
    "/participants/{participant_id}/visits",
    response_model=VisitResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_visit(
    participant_id: str,
    body: VisitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_write_access),
):
    """Creates a new consultation encounter (Clinician or Admin only)."""
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found",
        )

    visit_date = body.visit_date or datetime.now(timezone.utc)
    visit = Visit(
        participant_id=participant_id,
        visit_code=body.visit_code,
        visit_date=visit_date,
        follow_up_day=body.follow_up_day,
        wound_side=body.wound_side,
        anatomical_location=body.anatomical_location,
        notes=body.notes,
    )
    db.add(visit)
    db.commit()
    db.refresh(visit)

    log_audit_event(
        db,
        action="VISIT_CREATED",
        target_entity=f"Visit:{visit.id}",
        user_id=str(current_user.id),
        details={
            "study_id": participant.study_id,
            "visit_code": visit.visit_code,
            "follow_up_day": visit.follow_up_day,
        },
    )

    return visit

@router.get("/visits/{visit_id}", response_model=VisitResponse)
def get_visit(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieves visit encounter details."""
    v = db.query(Visit).filter(Visit.id == visit_id).first()
    if not v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found",
        )
    return v

@router.post(
    "/visits/{visit_id}/observations",
    response_model=ClinicalObservationResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_clinical_observation(
    visit_id: str,
    body: ClinicalObservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_write_access),
):
    """Attaches structured clinical observation findings to a visit."""
    v = db.query(Visit).filter(Visit.id == visit_id).first()
    if not v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Visit not found",
        )

    obs = ClinicalObservation(
        visit_id=visit_id,
        hba1c_percentage=body.hba1c_percentage,
        hba1c_date=body.hba1c_date,
        neuropathy_present=body.neuropathy_present,
        abi_index=body.abi_index,
        infection_status=body.infection_status,
        offloading_modality=body.offloading_modality,
        observation_source="clinician_entered",
        entered_by_user_id=str(current_user.id),
    )
    db.add(obs)
    db.commit()
    db.refresh(obs)

    log_audit_event(
        db,
        action="CLINICAL_OBSERVATION_RECORDED",
        target_entity=f"ClinicalObservation:{obs.id}",
        user_id=str(current_user.id),
        details={"visit_id": visit_id, "infection_status": obs.infection_status},
    )

    return obs

@router.get(
    "/visits/{visit_id}/observations",
    response_model=List[ClinicalObservationResponse],
)
def list_clinical_observations(
    visit_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Lists clinical observations for a visit encounter."""
    return (
        db.query(ClinicalObservation)
        .filter(ClinicalObservation.visit_id == visit_id)
        .all()
    )
