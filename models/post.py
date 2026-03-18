from unicodedata import category
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship, Column
from sqlalchemy import JSON
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from blogguide_user import BlogguideUser


class Post(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    blogguide_user_id: UUID = Field(foreign_key="blogguideuser.id", index=True)
    title: str = Field(index=True)
    content: str
    slug: str = Field(unique=True, index=True)
    subtitle: Optional[str] | None
    sections: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    description: Optional[str] | None
    icon: Optional[str] | None
    categoryLabel: Optional[str] | None
    categoryColor: Optional[str] | None
    category: Optional[str] | None
    excerpt: Optional[str] | None
    image_url: Optional[str] | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published: bool = Field(default=False)

    blogguide_user: "BlogguideUser" = Relationship(back_populates="posts")
