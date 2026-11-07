"""
Pydantic schemas for Security & Compliance Audit Logs.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AuditLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: Optional[str]
    action: str
    target_entity: str
    ip_address: Optional[str]
    details: Optional[str]
    timestamp: datetime

class AuditLogListResponse(BaseModel):
    total: int
    items: List[AuditLogResponse]
