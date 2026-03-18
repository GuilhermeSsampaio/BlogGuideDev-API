from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, List
from datetime import datetime


class PostRegister(BaseModel):
    title: str
    content: str
    subtitle: Optional[str] = None
    sections: Optional[List[dict]] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    published: Optional[bool] = False
    categoryLabel: Optional[str] = None
    categoryColor: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    subtitle: Optional[str] = None
    sections: Optional[List[dict]] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    published: Optional[bool] = None
    categoryLabel: Optional[str] = None
    categoryColor: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None


class PostResponse(BaseModel):
    id: UUID
    blogguide_user_id: UUID
    title: str
    content: str
    slug: str
    subtitle: Optional[str] = None
    sections: Optional[List[dict]] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    categoryLabel: Optional[str] = None
    categoryColor: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
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
    slug: str
    subtitle: Optional[str] = None
    sections: Optional[List[dict]] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    categoryLabel: Optional[str] = None
    categoryColor: Optional[str] = None
    icon: Optional[str] = None
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    author: PostAuthorResponse

    model_config = ConfigDict(from_attributes=True)
