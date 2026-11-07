"""
Clinical Observation Model.
Structured clinical data (HbA1c, neuropathy, vascular ABI, infection, offloading).
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class ClinicalObservation(Base):
    __tablename__ = "clinical_observations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(
        String(36), ForeignKey("visits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    
    # Biomarkers & Clinical Assessments
    hba1c_percentage = Column(Float, nullable=True)
    hba1c_date = Column(DateTime, nullable=True)
    neuropathy_present = Column(Boolean, nullable=True)
    abi_index = Column(Float, nullable=True)  # Ankle-Brachial Index
    infection_status = Column(
        String(50), default="none", nullable=False
    )  # none, superficial, deep, osteomyelitis
    offloading_modality = Column(
        String(100), default="removable_boot", nullable=False
    )  # total_contact_cast, removable_boot, therapeutic_shoes
    
    observation_source = Column(
        String(100), default="clinician_entered", nullable=False
    )
    entered_by_user_id = Column(String(36), ForeignKey("users.id"), nullable=True)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    visit = relationship("Visit", backref="clinical_observations")
