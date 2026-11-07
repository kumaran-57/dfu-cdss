"""
Pydantic schemas for Wound Segmentation, Calibrated Measurements & Uncertainty.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class AssessmentRequest(BaseModel):
    model_name: str = Field(default="segformer-b0", json_schema_extra={"example": "segformer-b0"})
    compute_uncertainty: bool = True

class PredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    image_id: str
    model_name: str
    model_version: str
    mask_path: Optional[str]
    pixel_area: int
    calibrated_area_cm2: Optional[float]
    major_length_mm: Optional[float]
    minor_width_mm: Optional[float]
    granulation_percentage: float
    slough_percentage: float
    necrotic_percentage: float
    uncertainty_score: float
    review_required: bool
    created_at: datetime
