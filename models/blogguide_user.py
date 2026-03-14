from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from auth.models.user import User
    from models.post import Post


class TipoPerfil(str, Enum):
    user = "user"
    admin = "admin"
    recrutador = "recrutador"


class BlogguideUser(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    user_id: UUID = Field(foreign_key="user.id", unique=True, index=True)
    tipo_perfil: str = Field(default=TipoPerfil.user)
    nome_completo: Optional[str] | None = None
    bio: Optional[str] | None = None
    profile_picture: Optional[str] | None = None
    empresa: Optional[str] | None = None
    github: Optional[str] | None = None
    linkedin: Optional[str] | None = None
    verified: Optional[bool] = Field(default=False)
    posts: list["Post"] = Relationship(back_populates="blogguide_user")

    user: "User" = Relationship(sa_relationship_kwargs={"uselist": False})
