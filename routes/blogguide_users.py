from typing import List
from fastapi import Depends, APIRouter, UploadFile, File, Form
from uuid import UUID

from auth.schemas.auth_schema import UserLogin, UserRegister
from auth.schemas.token_schema import TokenResponse
from auth.security.dependencies import current_user, require_role
from models.blogguide_user import TipoPerfil
from config.db import SessionDep

from schemas.blogguide_user_schema import (
    BlogguideUserResponse,
    BlogguideUserUpdate,
    UserStatsResponse,
)
from schemas.post_schema import (
    PostRegister,
    PostResponse,
    PostUpdate,
)

from services.user_service import (
    authenticate_blogguide_user,
    edit_profile,
    edit_profile_with_avatar,
    get_my_profile,
    get_user_stats,
    list_all_blogguide_users,
    register_blogguide_user,
    save_post_for_user,
    list_user_posts,
    update_user_post,
    delete_user_post,
)

router = APIRouter()


# ── Auth ────────────────────────────────────────────────────


@router.post("/register", response_model=BlogguideUserResponse)
def blogguide_user_register(user_data: UserRegister, session: SessionDep):
    return register_blogguide_user(session, user_data)


@router.post("/login", response_model=TokenResponse)
def blogguide_login(login_data: UserLogin, session: SessionDep):
    tokens = authenticate_blogguide_user(session, login_data.email, login_data.password)
    return {**tokens, "token_type": "bearer"}


# ── Perfil ──────────────────────────────────────────────────


@router.get("/list_blogguide_users", response_model=List[BlogguideUserResponse])
def get_blogguide_users(session: SessionDep):
    return list_all_blogguide_users(session)


@router.get("/me", response_model=BlogguideUserResponse)
def me(session: SessionDep, user_id: str = Depends(current_user)):
    return get_my_profile(session, UUID(user_id))


@router.get("/me/stats", response_model=UserStatsResponse)
def my_stats(session: SessionDep, user_id: str = Depends(current_user)):
    return get_user_stats(session, UUID(user_id))


@router.put("/edit_profile", response_model=BlogguideUserResponse)
def update_profile(
    updates: BlogguideUserUpdate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    return edit_profile(session, UUID(user_id), updates)


@router.put("/edit_profile_with_avatar", response_model=BlogguideUserResponse)
async def update_profile_with_avatar(
    session: SessionDep,
    user_id: str = Depends(current_user),
    nome_completo: str | None = Form(None),
    bio: str | None = Form(None),
    github: str | None = Form(None),
    linkedin: str | None = Form(None),
    avatar: UploadFile | None = File(None),
):
    # Endpoint dedicado a multipart/form-data para avatar.
    return await edit_profile_with_avatar(
        session,
        UUID(user_id),
        nome_completo,
        bio,
        github,
        linkedin,
        avatar,
    )


# ── Posts ────────────────────────────────────────────────


@router.post("/save_post", response_model=PostResponse)
def save_post(
    post_data: PostRegister,
    session: SessionDep,
    user_id: str = Depends(require_role(TipoPerfil.admin)),
):
    return save_post_for_user(session, UUID(user_id), post_data)


@router.get("/my_posts", response_model=List[PostResponse])
def get_my_posts(session: SessionDep, user_id: str = Depends(current_user)):
    return list_user_posts(session, UUID(user_id))


@router.put("/update_post/{post_id}", response_model=PostResponse)
def update_post(
    post_data: PostUpdate,
    session: SessionDep,
    post_id: str,
    user_id: str = Depends(require_role(TipoPerfil.admin)),
):
    return update_user_post(session, UUID(user_id), UUID(post_id), post_data)


@router.delete("/delete_post/{post_id}")
def delete_post(
    session: SessionDep,
    post_id: str,
    user_id: str = Depends(require_role(TipoPerfil.admin)),
):
    return delete_user_post(session, UUID(user_id), UUID(post_id))
