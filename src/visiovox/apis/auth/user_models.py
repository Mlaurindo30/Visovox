from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any

class User(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False

class UserInDB(User):
    hashed_password: str
    roles: List[str] = []

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenPayload(BaseModel):
    sub: str  # subject (username ou id)
    exp: int  # expiração unix timestamp
    scopes: List[str] = []

class UserProfile(BaseModel):
    username: str
    email: EmailStr
    roles: List[str] = []
    is_active: bool = True
    profile: Optional[Any] = None

class ErrorResponse(BaseModel):
    error_code: str
    message: str 