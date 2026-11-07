"""
Audit Log Model.
Maintains an immutable ledger of system operations for security and compliance.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from backend.app.core.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False, index=True)
    target_entity = Column(String(200), nullable=False)
    ip_address = Column(String(45), nullable=True)
    details = Column(Text, nullable=True)

    timestamp = Column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True
    )
