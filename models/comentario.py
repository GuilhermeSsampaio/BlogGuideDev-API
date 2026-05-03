from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from models.blogguide_user import BlogguideUser


class Comentario(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    conteudo: str
    data: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    autor_id: UUID = Field(foreign_key="blogguideuser.id", index=True)
    referencia_id: UUID = Field(index=True)
    tipo_referencia: str = Field(index=True)  # "post" ou "forum"
    parent_id: Optional[UUID] = Field(default=None, foreign_key="comentario.id", index=True)

    autor: "BlogguideUser" = Relationship()
