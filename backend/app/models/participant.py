"""
Participant and Consent models.
Stores coded research IDs without direct patient identifiers.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime
from backend.app.core.database import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    study_id = Column(String(50), unique=True, index=True, nullable=False)  # e.g. PART-001
    biological_sex = Column(String(20), nullable=True)  # female, male, other, undisclosed
    age_at_enrollment = Column(Integer, nullable=True)
    enrollment_status = Column(String(50), default="active", nullable=False)
    
    # Consent tracking
    consent_version = Column(String(50), default="v1.0", nullable=False)
    consent_status = Column(String(50), default="granted", nullable=False)  # granted, withdrawn
    consent_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
