from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from auth.models.user import User


class AuthProvider(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")

    provider: str
    provider_user_id: str | None = None
    password_hash: str | None = None

    user: "User" = Relationship(back_populates="providers")
