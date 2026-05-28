from pydantic import BaseModel, ConfigDict, EmailStr, field_validator
from uuid import UUID
from typing import Optional

from auth.schemas.auth_schema import (
    USERNAME_MIN_LENGTH,
    USERNAME_MAX_LENGTH,
    USERNAME_PATTERN,
)


class BlogguideUserUpdate(BaseModel):
    username: Optional[str] = None
    nome_completo: Optional[str] = None
    bio: Optional[str] = None
    profile_picture: Optional[str] = None
    empresa: Optional[str] = None
    cnpj: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    is_public: Optional[bool] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str | None) -> str | None:
        if v is None:
            return v
        v = v.strip().lower()
        if len(v) < USERNAME_MIN_LENGTH:
            raise ValueError(
                f"Username deve ter no mínimo {USERNAME_MIN_LENGTH} caracteres"
            )
        if len(v) > USERNAME_MAX_LENGTH:
            raise ValueError(
                f"Username deve ter no máximo {USERNAME_MAX_LENGTH} caracteres"
            )
        if not USERNAME_PATTERN.match(v):
            raise ValueError(
                "Username deve conter apenas letras, números, '.', '_' ou '-' (sem espaços)"
            )
        return v


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
    is_public: bool

    model_config = ConfigDict(from_attributes=True)


class UserStatsResponse(BaseModel):
    curtidas: int
    comentarios: int
    foruns: int
