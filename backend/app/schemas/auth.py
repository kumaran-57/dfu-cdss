"""
Pydantic schemas for authentication and user accounts.
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: str
    email: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    role: Optional[str] = None

class LoginRequest(BaseModel):
    email: str = Field(..., pattern=EMAIL_REGEX)
    password: str

class UserCreate(BaseModel):
    email: str = Field(..., pattern=EMAIL_REGEX)
    password: str
    full_name: Optional[str] = None
    role: str = "viewer"

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
