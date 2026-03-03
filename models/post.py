from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from blogguide_user import BlogguideUser


class Post(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    blogguide_user_id: UUID = Field(foreign_key="blogguideuser.id", index=True)
    title: str = Field(index=True)
    content: str
    excerpt: Optional[str] | None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    published: bool = Field(default=False)

    blogguide_user: "BlogguideUser" = Relationship(back_populates="posts")
