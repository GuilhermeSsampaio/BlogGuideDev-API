from sqlmodel import SQLModel
from typing import Optional

class LoginRequest(SQLModel):
    email: str
    password: str

class LoginResponse(SQLModel):
    access_token: str
    token_type: str
    user: dict

class RegisterRequest(SQLModel):
    name: str
    username: str
    email: str
    password: str
    bio: Optional[str] = None

class TokenData(SQLModel):
    email: Optional[str] = None