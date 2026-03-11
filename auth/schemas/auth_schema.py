from pydantic import EmailStr, BaseModel
from typing import Optional


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    tipo_perfil: Optional[str] = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str
