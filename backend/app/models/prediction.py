"""
Prediction Model.
Stores AI-generated wound segmentation masks, calibrated areas, and tissue percentages.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    image_id = Column(
        String(36), ForeignKey("images.id", ondelete="CASCADE"), nullable=False, index=True
    )
    model_name = Column(String(100), default="segformer-b0", nullable=False)
    model_version = Column(String(50), default="1.0.0", nullable=False)
    mask_path = Column(String(500), nullable=True)
    
    # 2D Calibrated Measurements
    pixel_area = Column(Integer, nullable=False)
    calibrated_area_cm2 = Column(Float, nullable=True)
    major_length_mm = Column(Float, nullable=True)
    minor_width_mm = Column(Float, nullable=True)
    
    # Tissue Breakdown Percentages
    granulation_percentage = Column(Float, default=0.0, nullable=False)
    slough_percentage = Column(Float, default=0.0, nullable=False)
    necrotic_percentage = Column(Float, default=0.0, nullable=False)
    
    # Epistemic Uncertainty & Routing Flag
    uncertainty_score = Column(Float, default=0.0, nullable=False)
    review_required = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    image = relationship("Image", backref="predictions")
