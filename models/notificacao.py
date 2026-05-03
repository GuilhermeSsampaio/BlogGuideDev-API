from uuid import UUID, uuid4
from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class Notificacao(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    destinatario_id: UUID = Field(foreign_key="blogguideuser.id", index=True)
    ator_id: UUID | None = Field(default=None, foreign_key="blogguideuser.id", index=True)
    tipo: str = Field(index=True)  # curtida | comentario | resposta
    referencia_id: UUID = Field(index=True)
    tipo_referencia: str = Field(index=True)
    mensagem: str
    lida: bool = Field(default=False, index=True)
    data_criacao: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), index=True)
