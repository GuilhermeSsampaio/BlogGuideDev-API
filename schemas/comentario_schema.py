from __future__ import annotations

from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import Field


class ComentarioCreate(BaseModel):
    conteudo: str


class ComentarioAuthorResponse(BaseModel):
    username: str
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ComentarioResponse(BaseModel):
    id: UUID
    conteudo: str
    data: datetime
    referencia_id: UUID
    tipo_referencia: str
    parent_id: Optional[UUID] = None
    autor: ComentarioAuthorResponse
    respostas: list["ComentarioResponse"] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


ComentarioResponse.model_rebuild()
