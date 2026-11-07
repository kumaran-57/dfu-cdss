"""
Calibration Record Model.
Stores geometric scale factors (mm/pixel) and color reference detections.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class CalibrationRecord(Base):
    __tablename__ = "calibration_records"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    image_id = Column(
        String(36), ForeignKey("images.id", ondelete="CASCADE"), nullable=False, index=True
    )
    marker_type = Column(
        String(50), default="circle_10mm", nullable=False
    )  # circle_10mm, checkerboard_20mm, manual_reference
    mm_per_pixel = Column(Float, nullable=False)
    calibration_confidence = Column(Float, default=1.0, nullable=False)
    color_card_detected = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    image = relationship("Image", backref="calibration_records")
