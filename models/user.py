from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .post import Post

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    username: str = Field(max_length=50, unique=True)
    email: str = Field(max_length=255, unique=True)
    password_hash: str = Field(max_length=255)  # Adicionado campo de senha
    bio: Optional[str] = Field(default=None, max_length=500)
    github_url: Optional[str] = Field(default=None, max_length=255)
    linkedin_url: Optional[str] = Field(default=None, max_length=255)
    avatar_url: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    # Relacionamento com Post
    posts: List["Post"] = Relationship(back_populates="author")

class UserCreate(SQLModel):
    name: str
    username: str
    email: str
    password: str  # Adicionado campo de senha
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    avatar_url: Optional[str] = None

class UserUpdate(SQLModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    avatar_url: Optional[str] = None

class UserResponse(SQLModel):
    id: int
    name: str
    username: str
    email: str
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    avatar_url: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserPublic(SQLModel):
    """Versão pública do usuário (sem informações sensíveis)"""
    id: int
    name: str
    username: str
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime