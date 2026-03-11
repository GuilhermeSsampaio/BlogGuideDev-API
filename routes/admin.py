from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from uuid import UUID
from pydantic import BaseModel

from auth.security.dependencies import require_role
from models.blogguide_user import TipoPerfil
from config.db import SessionDep
from helpers.profile_helpers import to_blogguide_response

from repository.crud import (
    list_blogguide_users,
    list_all_posts,
    list_forum_topics,
    admin_delete_post,
    admin_delete_user,
    update_user_role,
    delete_forum_topic,
    get_admin_stats,
)
from schemas.blogguide_user_schema import BlogguideUserResponse
from schemas.post_schema import PostPublicResponse, PostAuthorResponse, PostResponse


router = APIRouter()


class RoleUpdate(BaseModel):
    tipo_perfil: str


# ── Dashboard ──────────────────────────────────────────


@router.get("/stats")
def stats(
    session: SessionDep,
    _: str = Depends(require_role(TipoPerfil.admin)),
):
    return get_admin_stats(session)


# ── Users ──────────────────────────────────────────────


@router.get("/users", response_model=List[BlogguideUserResponse])
def list_users(
    session: SessionDep,
    _: str = Depends(require_role(TipoPerfil.admin)),
):
    profiles = list_blogguide_users(session)
    return [to_blogguide_response(p) for p in profiles]


@router.put("/users/{profile_id}/role", response_model=BlogguideUserResponse)
def change_role(
    profile_id: UUID,
    body: RoleUpdate,
    session: SessionDep,
    _: str = Depends(require_role(TipoPerfil.admin)),
):
    valid_roles = [r.value for r in TipoPerfil]
    if body.tipo_perfil not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role inválido. Opções: {valid_roles}",
        )
    profile = update_user_role(session, profile_id, body.tipo_perfil)
    if not profile:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return to_blogguide_response(profile)


@router.delete("/users/{profile_id}")
def delete_user(
    profile_id: UUID,
    session: SessionDep,
    admin_id: str = Depends(require_role(TipoPerfil.admin)),
):
    from repository.crud import get_blogguide_user_by_user_id
    admin_profile = get_blogguide_user_by_user_id(session, UUID(admin_id))
    if admin_profile and admin_profile.id == profile_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você não pode deletar a si mesmo",
        )
    deleted = admin_delete_user(session, profile_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário deletado com sucesso"}


# ── Posts ──────────────────────────────────────────────


@router.get("/posts")
def list_posts(
    session: SessionDep,
    _: str = Depends(require_role(TipoPerfil.admin)),
):
    posts = list_all_posts(session)
    result = []
    for p in posts:
        author_name = "Desconhecido"
        if p.blogguide_user and p.blogguide_user.user:
            author_name = p.blogguide_user.user.username
        result.append({
            "id": str(p.id),
            "title": p.title,
            "excerpt": p.excerpt,
            "published": p.published,
            "created_at": p.created_at.isoformat(),
            "author": author_name,
        })
    return result


@router.delete("/posts/{post_id}")
def delete_post(
    post_id: UUID,
    session: SessionDep,
    _: str = Depends(require_role(TipoPerfil.admin)),
):
    deleted = admin_delete_post(session, post_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    return {"message": "Post deletado com sucesso"}


# ── Forum ──────────────────────────────────────────────


@router.get("/forum")
def list_topics(
    session: SessionDep,
    _: str = Depends(require_role(TipoPerfil.admin)),
):
    topics = list_forum_topics(session)
    result = []
    for t in topics:
        author_name = "Desconhecido"
        if t.autor and t.autor.user:
            author_name = t.autor.user.username
        result.append({
            "id": str(t.id),
            "titulo": t.titulo,
            "tipo": t.tipo,
            "data_criacao": t.data_criacao.isoformat(),
            "autor": author_name,
        })
    return result


@router.delete("/forum/{topic_id}")
def delete_topic(
    topic_id: UUID,
    session: SessionDep,
    _: str = Depends(require_role(TipoPerfil.admin)),
):
    deleted = delete_forum_topic(session, topic_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tópico não encontrado")
    return {"message": "Tópico deletado com sucesso"}
