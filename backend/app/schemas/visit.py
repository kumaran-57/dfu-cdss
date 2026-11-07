"""
Pydantic schemas for Visit and Wound tracking.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class VisitCreate(BaseModel):
    visit_code: str = Field(..., json_schema_extra={"example": "V01"})
    visit_date: Optional[datetime] = None
    follow_up_day: int = Field(default=0, ge=0)
    wound_side: str = Field(default="left", json_schema_extra={"example": "left"})
    anatomical_location: str = Field(default="plantar_forefoot", json_schema_extra={"example": "plantar_forefoot"})
    notes: Optional[str] = None

class VisitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    participant_id: str
    visit_code: str
    visit_date: datetime
    follow_up_day: int
    wound_side: str
    anatomical_location: str
    notes: Optional[str]
    created_at: datetime

class VisitListResponse(BaseModel):
    total: int
    items: List[VisitResponse]
