from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser


def list_blogguide_users(session: Session) -> List[BlogguideUser]:
    return session.exec(select(BlogguideUser).options(joinedload(BlogguideUser.user))).all()


def get_blogguide_user_by_user_id(
    session: Session, user_uuid: UUID
) -> Optional[BlogguideUser]:
    """Busca perfil Blogguide pelo user_id (da tabela User). Retorna None se não existir."""
    return session.exec(
        select(BlogguideUser)
        .options(joinedload(BlogguideUser.user))
        .where(BlogguideUser.user_id == user_uuid)
    ).first()


def create_blogguide_user(session: Session, user_uuid: UUID, tipo_perfil: str = "user") -> BlogguideUser:
    """Cria um novo perfil Blogguide vinculado ao user_id."""
    profile = BlogguideUser(user_id=user_uuid, tipo_perfil=tipo_perfil, verified=False)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return session.exec(
        select(BlogguideUser)
        .options(joinedload(BlogguideUser.user))
        .where(BlogguideUser.id == profile.id)
    ).first()


def update_blogguide_user(session: Session, profile: BlogguideUser) -> BlogguideUser:
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile
