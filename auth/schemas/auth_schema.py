import re
from pydantic import EmailStr, BaseModel, field_validator
from typing import Optional

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 30
USERNAME_PATTERN = re.compile(r"^[a-z0-9._-]+$")


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    tipo_perfil: Optional[str] = "user"
    nome_completo: Optional[str] = None
    bio: Optional[str] = None
    cnpj: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
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


class UserLogin(BaseModel):
    email: EmailStr
    password: str
