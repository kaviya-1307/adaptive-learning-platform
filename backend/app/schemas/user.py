from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=2, max_length=100)


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: str = "STUDENT"
    created_at: datetime
    onboarding_completed: bool = False
    learning_goal: Optional[str] = None
    experience_level: Optional[str] = None
    diagnostic_completed: bool = False
    diagnostic_exempt: bool = False
    diagnostic_score: Optional[int] = None
    diagnostic_total: Optional[int] = None
    diagnostic_completed_at: Optional[datetime] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Optional[UserResponse] = None


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    exp: Optional[int] = None
