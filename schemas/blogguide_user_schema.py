from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID
from typing import Optional


class BlogguideUserUpdate(BaseModel):
    nome_completo: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    empresa: Optional[str] = None
    cnpj: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None


class RoleUpdate(BaseModel):
    tipo_perfil: str


class BlogguideUserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    user_id: UUID
    tipo_perfil: str
    nome_completo: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    empresa: Optional[str] = None
    cnpj: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    verified: bool

    model_config = ConfigDict(from_attributes=True)


class UserStatsResponse(BaseModel):
    curtidas: int
    comentarios: int
    foruns: int
