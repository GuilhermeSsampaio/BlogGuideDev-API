from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session, func
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser
from models.curtida import Curtida
from models.comentario import Comentario
from models.forum import Forum


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


def create_blogguide_user(
    session: Session,
    user_uuid: UUID,
    tipo_perfil: str = "user",
    nome_completo: Optional[str] = None,
    bio: Optional[str] = None
) -> BlogguideUser:
    """Cria um novo perfil Blogguide vinculado ao user_id."""
    profile = BlogguideUser(
        user_id=user_uuid,
        tipo_perfil=tipo_perfil,
        nome_completo=nome_completo,
        bio=bio,
        verified=False
    )
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


def count_user_stats(session: Session, profile_id: UUID) -> dict:
    """Conta curtidas dadas, comentarios feitos e topicos criados pelo usuario."""
    curtidas = session.exec(
        select(func.count(Curtida.id)).where(Curtida.usuario_id == profile_id)
    ).one()
    comentarios = session.exec(
        select(func.count(Comentario.id)).where(Comentario.autor_id == profile_id)
    ).one()
    foruns = session.exec(
        select(func.count(Forum.id)).where(Forum.autor_id == profile_id)
    ).one()
    return {"curtidas": curtidas, "comentarios": comentarios, "foruns": foruns}
