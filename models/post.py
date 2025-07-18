from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    category: str = Field(max_length=100)
    content: str
    author_id: int = Field(foreign_key="user.id")
    image_url: Optional[str] = Field(default=None, max_length=255)
    tags: Optional[str] = Field(default=None)  # JSON string para as tags
    likes_count: int = Field(default=0)
    is_published: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Relacionamento com User
    author: Optional["User"] = Relationship(back_populates="posts")

class PostCreate(SQLModel):
    title: str
    category: str
    content: str
    author_id: int
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None

class PostUpdate(SQLModel):
    title: Optional[str] = None
    category: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    is_published: Optional[bool] = None

class PostResponse(SQLModel):
    id: int
    title: str
    category: str
    content: str
    author_id: int
    author: Optional["UserPublic"] = None
    image_url: Optional[str] = None
    tags: Optional[List[str]] = None
    likes_count: int
    is_published: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

# Importar UserPublic para evitar problemas de import circular
from .user import UserPublic