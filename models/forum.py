from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship, Column, JSON
from typing import Optional, TYPE_CHECKING, List
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
    data_atualizacao: Optional[datetime] = None
    tags: Optional[List[str]] = Field(default=[], sa_column=Column(JSON))
    autor_id: UUID = Field(foreign_key="blogguideuser.id", index=True)

    autor: "BlogguideUser" = Relationship()
