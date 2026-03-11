from typing import List
from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from config.db import SessionDep
from repository.crud import list_published_posts, get_published_post_by_id
from schemas.post_schema import PostPublicResponse, PostAuthorResponse

router = APIRouter()


def _to_public_response(post) -> PostPublicResponse:
    """Converte um Post (com blogguide_user.user carregados) em PostPublicResponse."""
    return PostPublicResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        excerpt=post.excerpt,
        image_url=post.image_url,
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
def get_published_post(post_id: UUID, session: SessionDep):
    """Retorna um conteúdo publicado pelo ID (rota pública)."""
    post = get_published_post_by_id(session, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteúdo não encontrado",
        )
    return _to_public_response(post)
