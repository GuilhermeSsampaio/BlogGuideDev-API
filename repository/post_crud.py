from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload
import re

from models.blogguide_user import BlogguideUser
from models.post import Post


def _generate_slug(title: str) -> str:
    """Gera um slug a partir do título."""
    slug = title.lower().strip()
    slug = re.sub(r'[à-ú]', lambda m: {
        'à': 'a', 'á': 'a', 'ã': 'a', 'â': 'a',
        'è': 'e', 'é': 'e', 'ê': 'e',
        'ì': 'i', 'í': 'i', 'î': 'i',
        'ò': 'o', 'ó': 'o', 'õ': 'o', 'ô': 'o',
        'ù': 'u', 'ú': 'u', 'û': 'u',
        'ç': 'c',
    }.get(m.group(0), m.group(0)), slug)
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = re.sub(r'^-+|-+$', '', slug)
    return slug


def create_post(session: Session, blogguide_user_id: UUID, post_data) -> Post:
    """Cria um novo post."""
    slug = _generate_slug(post_data.title)
    post = Post(
        blogguide_user_id=blogguide_user_id,
        title=post_data.title,
        content=post_data.content,
        subtitle=post_data.subtitle,
        sections=post_data.sections,
        excerpt=post_data.excerpt,
        image_url=post_data.image_url,
        published=post_data.published,
        slug=slug,
        categoryLabel=post_data.categoryLabel,
        categoryColor=post_data.categoryColor,
        icon=post_data.icon,
        description=post_data.description,
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


def get_post_by_slug(session: Session, slug: str) -> Optional[Post]:
    """Busca um post pelo slug, com dados do autor."""
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .where(Post.slug == slug)
    ).first()
