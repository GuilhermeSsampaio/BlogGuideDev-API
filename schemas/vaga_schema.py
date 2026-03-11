from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional
from datetime import datetime


class VagaCreate(BaseModel):
    titulo: str
    descricao: str
    empresa: str
    localidade: Optional[str] = None
    tipo_contrato: Optional[str] = None
    link: Optional[str] = None


class VagaUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    empresa: Optional[str] = None
    localidade: Optional[str] = None
    tipo_contrato: Optional[str] = None
    link: Optional[str] = None
    ativa: Optional[bool] = None


class VagaRecrutadorResponse(BaseModel):
    username: str
    empresa: Optional[str] = None
    profile_picture: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class VagaResponse(BaseModel):
    id: UUID
    titulo: str
    descricao: str
    empresa: str
    localidade: Optional[str] = None
    tipo_contrato: Optional[str] = None
    link: Optional[str] = None
    ativa: bool
    data_criacao: datetime
    recrutador: VagaRecrutadorResponse

    model_config = ConfigDict(from_attributes=True)
