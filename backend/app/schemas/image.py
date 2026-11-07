"""
Pydantic schemas for Image uploads and quality verification.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    visit_id: str
    file_path: str
    mime_type: str
    width: int
    height: int
    sha256_hash: str
    view_label: str
    quality_passed: bool
    blur_score: Optional[float]
    exposure_status: str
    is_synthetic: bool
    created_at: datetime

class ImageQualityCheckResponse(BaseModel):
    image_id: str
    quality_passed: bool
    blur_score: float
    is_blurry: bool
    exposure_status: str
    recommendations: List[str]
