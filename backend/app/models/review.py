"""
Clinician Review Model.
Stores clinician verification, overrides, and timestamps for AI predictions.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class ClinicianReview(Base):
    __tablename__ = "clinician_reviews"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    prediction_id = Column(
        String(36), ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    clinician_id = Column(
        String(36), ForeignKey("users.id"), nullable=False, index=True
    )
    approved = Column(Boolean, default=True, nullable=False)
    override_area_cm2 = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    prediction = relationship("Prediction", backref="clinician_reviews")
    clinician = relationship("User", backref="reviews_performed")
