from pydantic import EmailStr, BaseModel
from typing import Optional


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    tipo_perfil: Optional[str] = "user"
    nome_completo: Optional[str] = None
    bio: Optional[str] = None
    cnpj: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str
