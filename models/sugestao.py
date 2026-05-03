from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Sugestao(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID | None = Field(default=None, foreign_key="blogguideuser.id", index=True)
    tipo: str = Field(index=True)  # sugestao | bug
    titulo: str = Field(index=True)
    descricao: str
    email_contato: str | None = None
    canal_contato: str | None = None  # email | whatsapp
    status: str = Field(default="aberta", index=True)
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
