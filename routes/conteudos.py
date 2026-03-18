from typing import List
from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from config.db import SessionDep
from repository.crud import list_published_posts, get_published_post_by_id, get_post_by_slug
from schemas.post_schema import PostPublicResponse, PostAuthorResponse

router = APIRouter()


def _to_public_response(post) -> PostPublicResponse:
    """Converte um Post (com blogguide_user.user carregados) em PostPublicResponse."""
    return PostPublicResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        slug=post.slug,
        subtitle=post.subtitle,
        sections=post.sections,
        excerpt=post.excerpt,
        image_url=post.image_url,
        categoryLabel=post.categoryLabel,
        categoryColor=post.categoryColor,
        icon=post.icon,
        description=post.description,
        created_at=post.created_at,
        updated_at=post.updated_at,
        author=PostAuthorResponse(
            username=post.blogguide_user.user.username,
            profile_picture=post.blogguide_user.profile_picture,
        ),
    )


@router.get("/", response_model=List[PostPublicResponse])
def get_all_published_posts(session: SessionDep):
    """Lista todos os conteúdos publicados (rota pública)."""
    posts = list_published_posts(session)
    return [_to_public_response(p) for p in posts]


@router.get("/{post_id}", response_model=PostPublicResponse)
def get_published_post(post_id: str, session: SessionDep):
    """Retorna um conteúdo publicado pelo ID ou slug (rota pública)."""
    post = None

    # Tenta primeiro como UUID
    try:
        uuid_id = UUID(post_id)
        post = get_published_post_by_id(session, uuid_id)
    except (ValueError, TypeError):
        # Se não for UUID, tenta como slug
        post = get_post_by_slug(session, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado",
        )
    return _to_public_response(post)
