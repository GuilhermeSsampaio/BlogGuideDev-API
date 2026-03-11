from pydantic import BaseModel, ConfigDict
from uuid import UUID


class CurtidaToggleResponse(BaseModel):
    curtido: bool
    total: int


class CurtidaCountResponse(BaseModel):
    total: int
    curtido_por_usuario: bool = False
