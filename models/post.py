from unicodedata import category
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    category: str
    content: str
    author: str = Field(max_length=100)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

class PostCreate(SQLModel):
    title: str
    category: str
    content: str
    author: str

class PostResponse(SQLModel):
    id: int
    title: str
    category: str
    content: str
    author: str
    created_at: datetime
    updated_at: Optional[datetime] = None