from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime


class ForumCreate(BaseModel):
    titulo: str
    descricao: str
    tipo: Optional[str] = None


class ForumUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    tipo: Optional[str] = None


class ForumAuthorResponse(BaseModel):
    username: str
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ForumResponse(BaseModel):
    id: UUID
    titulo: str
    descricao: str
    tipo: Optional[str] = None
    data_criacao: datetime
    autor: ForumAuthorResponse

    model_config = ConfigDict(from_attributes=True)
