"""
Visit and Wound Models.
Represents discrete clinical consultation encounters and wound tracking.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Visit(Base):
    __tablename__ = "visits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    participant_id = Column(
        String(36), ForeignKey("participants.id", ondelete="CASCADE"), nullable=False, index=True
    )
    visit_code = Column(String(50), nullable=False)  # e.g. V01, V02
    visit_date = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    follow_up_day = Column(Integer, default=0, nullable=False)  # Days elapsed since baseline
    wound_side = Column(String(20), default="left", nullable=False)  # left, right
    anatomical_location = Column(
        String(100), default="plantar_forefoot", nullable=False
    )
    notes = Column(Text, nullable=True)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    # Relationships
    participant = relationship("Participant", backref="visits")
