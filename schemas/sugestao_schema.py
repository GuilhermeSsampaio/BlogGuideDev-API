from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SugestaoCreate(BaseModel):
    tipo: str
    titulo: str
    descricao: str
    email_contato: str | None = None
    canal_contato: str | None = None


class SugestaoResponse(BaseModel):
    id: UUID
    user_id: UUID | None
    tipo: str
    titulo: str
    descricao: str
    email_contato: str | None
    canal_contato: str | None
    status: str
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)
