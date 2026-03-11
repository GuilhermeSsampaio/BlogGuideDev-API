from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from models.blogguide_user import BlogguideUser


class Vaga(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    titulo: str = Field(index=True)
    descricao: str
    empresa: str
    localidade: Optional[str] = None
    tipo_contrato: Optional[str] = None  # CLT, PJ, Estágio, Freelance
    link: Optional[str] = None
    ativa: bool = Field(default=True)
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    recrutador_id: UUID = Field(foreign_key="blogguideuser.id", index=True)

    recrutador: "BlogguideUser" = Relationship()
