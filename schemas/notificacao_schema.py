from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class NotificacaoResponse(BaseModel):
    id: UUID
    tipo: str
    referencia_id: UUID
    tipo_referencia: str
    mensagem: str
    lida: bool
    data_criacao: datetime

    model_config = ConfigDict(from_attributes=True)


class NotificacaoListResponse(BaseModel):
    unread_count: int
    items: list[NotificacaoResponse]


class NotificacaoReadResponse(BaseModel):
    success: bool
    notificacao: NotificacaoResponse | None = None
