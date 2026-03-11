from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser
from models.post import Post


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


def create_blogguide_user(session: Session, user_uuid: UUID) -> BlogguideUser:
    """Cria um novo perfil Blogguide vinculado ao user_id."""
    profile = BlogguideUser(user_id=user_uuid, verified=False)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    # Recarrega com relationship
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


def create_post(session: Session, blogguide_user_id: UUID, post_data) -> Post:
    """Cria um novo post."""
    post = Post(
        blogguide_user_id=blogguide_user_id,
        title=post_data.title,
        content=post_data.content,
        excerpt=post_data.excerpt,
        published=post_data.published,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_post_by_id(session: Session, post_id: UUID) -> Optional[Post]:
    """Busca um post pelo ID."""
    return session.exec(select(Post).where(Post.id == post_id)).first()


def get_user_posts(session: Session, user_id: UUID) -> List[Post]:
    """Busca todos os posts de um usuário."""
    return session.exec(
        select(Post)
        .where(Post.blogguide_user_id == user_id)
    ).all()


def update_post(session: Session, post: Post) -> Post:
    """Atualiza um post."""
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def delete_post(session: Session, post_id: UUID) -> bool:
    """Deleta um post. Retorna True se foi deletado, False se não encontrou."""
    post = get_post_by_id(session, post_id)
    if post:
        session.delete(post)
        session.commit()
        return True
    return False


def list_published_posts(session: Session) -> List[Post]:
    """Lista todos os posts publicados, com dados do autor."""
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .where(Post.published == True)
        .order_by(Post.created_at.desc())
    ).all()


def get_published_post_by_id(session: Session, post_id: UUID) -> Optional[Post]:
    """Busca um post publicado pelo ID, com dados do autor."""
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .where(Post.id == post_id, Post.published == True)
    ).first()
