"""
Pydantic schemas for Clinical Observations.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ClinicalObservationCreate(BaseModel):
    hba1c_percentage: Optional[float] = Field(None, ge=3.5, le=20.0)
    hba1c_date: Optional[datetime] = None
    neuropathy_present: Optional[bool] = None
    abi_index: Optional[float] = Field(None, ge=0.1, le=3.0)
    infection_status: str = Field(default="none", json_schema_extra={"example": "none"})
    offloading_modality: str = Field(default="removable_boot", json_schema_extra={"example": "removable_boot"})

class ClinicalObservationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    visit_id: str
    hba1c_percentage: Optional[float]
    hba1c_date: Optional[datetime]
    neuropathy_present: Optional[bool]
    abi_index: Optional[float]
    infection_status: str
    offloading_modality: str
    observation_source: str
    created_at: datetime
