"""
Authentication API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from backend.app.core.database import get_db
from backend.app.models.user import User
from backend.app.schemas.auth import LoginRequest, Token, UserResponse
from backend.app.security.password import verify_password
from backend.app.security.auth import create_access_token, get_current_user
from backend.app.services.audit import log_audit_event

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(request: Request, body: LoginRequest, db: Session = Depends(get_db)):
    """Authenticates credentials and returns a secure JWT bearer token."""
    user = db.query(User).filter(User.email == body.email).first()
    ip_addr = request.client.host if request.client else None

    if not user or not verify_password(body.password, user.hashed_password):
        log_audit_event(
            db,
            action="LOGIN_FAILED",
            target_entity=f"User:{body.email}",
            ip_address=ip_addr,
            details={"reason": "Invalid credentials"},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated",
        )

    token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.role}
    )

    log_audit_event(
        db,
        action="LOGIN_SUCCESS",
        target_entity=f"User:{user.email}",
        user_id=str(user.id),
        ip_address=ip_addr,
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role,
        "user_id": str(user.id),
        "email": user.email,
    }

@router.get("/me", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    """Returns currently authenticated user profile."""
    return current_user
