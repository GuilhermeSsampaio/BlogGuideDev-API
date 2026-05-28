from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class PushSubscription(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="blogguideuser.id", index=True)
    endpoint: str = Field(index=True, unique=True)
    p256dh: str
    auth: str
    expiration_time: float | None = Field(default=None)
    user_agent: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), index=True
    )
