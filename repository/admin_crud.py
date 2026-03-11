from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload
from sqlalchemy import func

from models.blogguide_user import BlogguideUser
from models.post import Post
from models.forum import Forum
from models.comentario import Comentario
from models.curtida import Curtida
from auth.models.user import User
from auth.models.auth_provider import AuthProvider

from repository.post_crud import get_post_by_id


def list_all_posts(session: Session) -> List[Post]:
    """Lista todos os posts (publicados e rascunhos) com dados do autor."""
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .order_by(Post.created_at.desc())
    ).all()


def admin_delete_post(session: Session, post_id: UUID) -> bool:
    """Admin: deleta qualquer post pelo ID."""
    post = get_post_by_id(session, post_id)
    if post:
        session.delete(post)
        session.commit()
        return True
    return False


def update_user_role(session: Session, profile_id: UUID, new_role: str) -> Optional[BlogguideUser]:
    """Atualiza o tipo_perfil de um usuário."""
    profile = session.get(BlogguideUser, profile_id)
    if not profile:
        return None
    profile.tipo_perfil = new_role
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return session.exec(
        select(BlogguideUser)
        .options(joinedload(BlogguideUser.user))
        .where(BlogguideUser.id == profile.id)
    ).first()


def admin_delete_user(session: Session, profile_id: UUID) -> bool:
    """Admin: deleta um perfil blogguide e o user base associado."""
    profile = session.get(BlogguideUser, profile_id)
    if not profile:
        return False
    user = session.get(User, profile.user_id)

    # Deletar posts do perfil
    posts = session.exec(select(Post).where(Post.blogguide_user_id == profile.id)).all()
    for post in posts:
        session.delete(post)

    # Deletar forum topics
    topics = session.exec(select(Forum).where(Forum.autor_id == profile.id)).all()
    for topic in topics:
        session.delete(topic)

    # Deletar comentários
    comentarios = session.exec(select(Comentario).where(Comentario.autor_id == profile.id)).all()
    for c in comentarios:
        session.delete(c)

    # Deletar curtidas
    curtidas = session.exec(select(Curtida).where(Curtida.usuario_id == profile.id)).all()
    for c in curtidas:
        session.delete(c)

    # Deletar auth providers
    providers = session.exec(select(AuthProvider).where(AuthProvider.user_id == profile.user_id)).all()
    for p in providers:
        session.delete(p)

    session.delete(profile)
    if user:
        session.delete(user)

    session.commit()
    return True


def get_admin_stats(session: Session) -> dict:
    """Retorna estatísticas gerais do sistema."""
    total_users = session.exec(select(func.count(BlogguideUser.id))).one()
    total_posts = session.exec(select(func.count(Post.id))).one()
    published_posts = session.exec(
        select(func.count(Post.id)).where(Post.published == True)
    ).one()
    total_topics = session.exec(select(func.count(Forum.id))).one()
    total_comentarios = session.exec(select(func.count(Comentario.id))).one()
    total_curtidas = session.exec(select(func.count(Curtida.id))).one()
    return {
        "total_users": total_users,
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": total_posts - published_posts,
        "total_topics": total_topics,
        "total_comentarios": total_comentarios,
        "total_curtidas": total_curtidas,
    }
