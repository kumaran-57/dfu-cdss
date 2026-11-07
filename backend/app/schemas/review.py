"""
Pydantic schemas for Clinician Review and Overrides.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ClinicianReviewCreate(BaseModel):
    approved: bool
    override_area_cm2: Optional[float] = Field(None, ge=0.0)
    notes: Optional[str] = None

class ClinicianReviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    prediction_id: str
    clinician_id: str
    approved: bool
    override_area_cm2: Optional[float]
    notes: Optional[str]
    created_at: datetime
