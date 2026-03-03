from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from auth.models.auth_provider import AuthProvider
from auth.models.user import User
from auth.schemas.auth_schema import UserRegister
from auth.security.hashing import hash_password
from auth.services.auth_service import login_user

from helpers.profile_helpers import (
    get_profile_or_404,
    to_blogguide_response
)
from repository.crud import *
from schemas.blogguide_user_schema import (
    BlogguideUserResponse, BlogguideUserUpdate
)
from schemas.post_schema import (
    PostRegister, PostResponse, PostUpdate
)


def register_blogguide_user(
    session: Session, user_data: UserRegister
) -> BlogguideUserResponse:
    """Cria User base + AuthProvider + blogguideUser."""
    try:
        user_base = User(username=user_data.username, email=user_data.email)
        session.add(user_base)
        session.commit()
        session.refresh(user_base)
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ou username já cadastrado",
        )

    auth_provider = AuthProvider(
        user_id=user_base.id,
        provider="password",
        password_hash=hash_password(user_data.password),
    )
    session.add(auth_provider)
    session.commit()

    profile = create_blogguide_user(session, user_base.id)
    return to_blogguide_response(profile)


def authenticate_blogguide_user(session: Session, email: str, password: str) -> dict:
    """Autentica e retorna access_token + refresh_token ou lança 401."""
    tokens = login_user(session, email, password)

    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
        )

    return tokens


def list_all_blogguide_users(session: Session) -> list[BlogguideUserUpdate]:
    """Lista todos os perfis blogguide."""
    profiles = list_blogguide_users(session)
    return [to_blogguide_response(p) for p in profiles]


def get_my_profile(session: Session, user_uuid: UUID) -> BlogguideUserUpdate:
    """Busca perfil do usuário autenticado. Cria se não existir (OAuth)."""
    profile = get_blogguide_user_by_user_id(session, user_uuid)

    if not profile:
        profile = create_blogguide_user(session, user_uuid)

    return to_blogguide_response(profile)


def edit_profile(
    session: Session, user_uuid: UUID, updates: BlogguideUserUpdate
) -> BlogguideUserUpdate:
    """Atualiza o perfil do usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)

    if updates.bio is not None:
        profile.bio = updates.bio

    profile = update_blogguide_user(session, profile)
    return to_blogguide_response(profile)


def save_post_for_user(
    session: Session, user_uuid: UUID, post_data: PostRegister
) -> PostResponse:
    """Cria um novo post para o usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)
    post = create_post(session, profile.id, post_data)
    return PostResponse.model_validate(post)


def list_user_posts(session: Session, user_uuid: UUID) -> list[PostResponse]:
    """Lista todos os posts do usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)
    posts = get_user_posts(session, profile.id)
    return [PostResponse.model_validate(post) for post in posts]


def update_user_post(
    session: Session, user_uuid: UUID, post_id: UUID, post_data: PostUpdate
) -> PostResponse:
    """Atualiza um post do usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)
    post = get_post_by_id(session, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post não encontrado",
        )

    if post.blogguide_user_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar este post",
        )

    if post_data.title is not None:
        post.title = post_data.title
    if post_data.content is not None:
        post.content = post_data.content
    if post_data.excerpt is not None:
        post.excerpt = post_data.excerpt
    if post_data.published is not None:
        post.published = post_data.published

    post = update_post(session, post)
    return PostResponse.model_validate(post)


def delete_user_post(session: Session, user_uuid: UUID, post_id: UUID) -> dict:
    """Deleta um post do usuário autenticado."""
    profile = get_profile_or_404(session, user_uuid)
    post = get_post_by_id(session, post_id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post não encontrado",
        )

    if post.blogguide_user_id != profile.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar este post",
        )

    delete_post(session, post_id)
    return {"message": "Post deletado com sucesso"}
