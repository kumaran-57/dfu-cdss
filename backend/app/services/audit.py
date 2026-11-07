"""
Audit logging service for regulatory compliance and access tracking.
"""

import json
from typing import Optional, Any
from sqlalchemy.orm import Session
from backend.app.models.audit import AuditLog

def log_audit_event(
    db: Session,
    action: str,
    target_entity: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    details: Optional[Any] = None,
) -> AuditLog:
    """Creates an immutable audit log record."""
    details_str = None
    if details is not None:
        if isinstance(details, (dict, list)):
            details_str = json.dumps(details, default=str)
        else:
            details_str = str(details)

    log_entry = AuditLog(
        user_id=user_id,
        action=action,
        target_entity=target_entity,
        ip_address=ip_address,
        details=details_str,
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
