"""
Pydantic schemas for Participant management.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ParticipantCreate(BaseModel):
    study_id: str = Field(..., pattern=r"^PART-[A-Z0-9_-]+$")
    biological_sex: Optional[str] = "undisclosed"
    age_at_enrollment: Optional[int] = Field(None, ge=18, le=120)
    enrollment_status: str = "active"
    consent_version: str = "v1.0"

class ParticipantUpdate(BaseModel):
    biological_sex: Optional[str] = None
    age_at_enrollment: Optional[int] = Field(None, ge=18, le=120)
    enrollment_status: Optional[str] = None
    consent_status: Optional[str] = None

class ParticipantResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    study_id: str
    biological_sex: Optional[str]
    age_at_enrollment: Optional[int]
    enrollment_status: str
    consent_version: str
    consent_status: str
    consent_date: datetime
    created_at: datetime
    updated_at: datetime

class ParticipantListResponse(BaseModel):
    total: int
    items: List[ParticipantResponse]
