from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.blogguide_user import BlogguideUser


class Curtida(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    usuario_id: UUID = Field(foreign_key="blogguideuser.id", index=True)
    referencia_id: UUID = Field(index=True)
    tipo_referencia: str = Field(index=True)  # "post", "forum" ou "comentario"

    usuario: "BlogguideUser" = Relationship()
