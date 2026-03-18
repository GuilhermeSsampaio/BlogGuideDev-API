from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel


class Conteudo(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    slug: str = Field(unique=True, index=True)
    titulo: str
