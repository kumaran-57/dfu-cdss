"""
Image Model.
Tracks de-identified wound images, validation status, and file paths.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    visit_id = Column(
        String(36), ForeignKey("visits.id", ondelete="CASCADE"), nullable=False, index=True
    )
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(50), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    sha256_hash = Column(String(64), nullable=False, index=True)
    view_label = Column(String(50), default="dorsal_aspect", nullable=False)
    
    # Image Quality Checks
    quality_passed = Column(Boolean, default=True, nullable=False)
    blur_score = Column(Float, nullable=True)  # Laplacian variance
    exposure_status = Column(String(50), default="normal", nullable=False)
    
    # Research & synthetic tracking
    is_synthetic = Column(Boolean, default=False, nullable=False)

    created_at = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    visit = relationship("Visit", backref="images")
