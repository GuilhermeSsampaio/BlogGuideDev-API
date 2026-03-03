from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from typing import Optional


class BlogguideUserUpdate(BaseModel):
    bio: Optional[str] = None
    profile_picture: Optional[str] = None


class BlogguideUserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    user_id: UUID
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    verified: bool

    model_config = ConfigDict(from_attributes=True)
