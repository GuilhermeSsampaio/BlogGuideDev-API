from pydantic import BaseModel, ConfigDict
from uuid import UUID


class ConteudoResponse(BaseModel):
    id: UUID
    slug: str
    titulo: str

    model_config = ConfigDict(from_attributes=True)
