"""
User Administration API (Admin only).
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User, UserRole
from backend.app.schemas.auth import UserCreate, UserResponse
from backend.app.security.auth import RoleChecker
from backend.app.security.password import get_password_hash
from backend.app.services.audit import log_audit_event

router = APIRouter(prefix="/users", tags=["User Administration"])

require_admin = RoleChecker(["admin"])

@router.get("", response_model=List[UserResponse])
def list_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Lists all registered users (Admin only)."""
    return db.query(User).all()

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin),
):
    """Registers a new authorized user with designated role (Admin only)."""
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists",
        )

    # Validate allowed role
    valid_roles = [r.value for r in UserRole]
    if body.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {valid_roles}",
        )

    new_user = User(
        email=body.email,
        hashed_password=get_password_hash(body.password),
        full_name=body.full_name,
        role=body.role,
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    log_audit_event(
        db,
        action="USER_CREATED",
        target_entity=f"User:{new_user.email}",
        user_id=str(admin_user.id),
        details={"assigned_role": new_user.role},
    )

    return new_user
