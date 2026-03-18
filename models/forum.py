from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from models.blogguide_user import BlogguideUser


class Forum(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    titulo: str = Field(index=True)
    descricao: str
    tipo: Optional[str] = None
    imagem_url: Optional[str] = None
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    autor_id: UUID = Field(foreign_key="blogguideuser.id", index=True)

    autor: "BlogguideUser" = Relationship()
