from typing import List
from fastapi import Depends, APIRouter
from uuid import UUID

from auth.schemas.auth_schema import UserLogin, UserRegister
from auth.schemas.token_schema import TokenResponse
from auth.security.dependencies import current_user
from config.db import SessionDep

from schemas.blogguide_user_schema import (
    BlogguideUserResponse,
    BlogguideUserUpdate,
)
from schemas.post_schema import (
    PostRegister,
    PostResponse,
    PostUpdate,
)

from services.user_service import (
    authenticate_blogguide_user,
    edit_profile,
    get_my_profile,
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


@router.put("/edit_profile", response_model=BlogguideUserResponse)
def update_profile(
    updates: BlogguideUserUpdate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    return edit_profile(session, UUID(user_id), updates)


# ── Posts ────────────────────────────────────────────────


@router.post("/save_post", response_model=PostResponse)
def save_post(
    post_data: PostRegister,
    session: SessionDep,
    user_id: str = Depends(current_user),
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
    user_id: str = Depends(current_user),
):
    return update_user_post(session, UUID(user_id), UUID(post_id), post_data)


@router.delete("/delete_post/{post_id}")
def delete_post(
    session: SessionDep,
    post_id: str,
    user_id: str = Depends(current_user),
):
    return delete_user_post(session, UUID(user_id), UUID(post_id))
