from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime


class PostRegister(BaseModel):
    title: str
    content: str
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    published: Optional[bool] = False


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    published: Optional[bool] = None


class PostResponse(BaseModel):
    id: UUID
    blogguide_user_id: UUID
    title: str
    content: str
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    published: bool

    model_config = ConfigDict(from_attributes=True)


class PostAuthorResponse(BaseModel):
    username: str
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PostPublicResponse(BaseModel):
    id: UUID
    title: str
    content: str
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author: PostAuthorResponse

    model_config = ConfigDict(from_attributes=True)
