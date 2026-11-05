"""
Pydantic Schemas for Users & Authentication
"""
from typing import Optional
from pydantic import BaseModel, Field


class UserRegisterRequest(BaseModel):
    email: str
    password: str = Field(..., min_length=6)
    full_name: str
    role: Optional[str] = "User"


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    avatar_url: Optional[str] = None
    role: str
    is_active: bool
    created_at: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
