from typing import List
from fastapi import Depends, APIRouter
from uuid import UUID

from auth.security.dependencies import current_user
from config.db import SessionDep

from schemas.post_schema import (
    PostRegister,
    PostResponse,
    PostUpdate,
)

from services.user_service import (
    save_post_for_user,
    list_user_posts,
    update_user_post,
    delete_user_post,
)

router = APIRouter()


@router.post("/create", response_model=PostResponse)
def create_post(
    post_data: PostRegister,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    return save_post_for_user(session, UUID(user_id), post_data)


@router.get("/my_posts", response_model=List[PostResponse])
def get_my_posts(session: SessionDep, user_id: str = Depends(current_user)):
    return list_user_posts(session, UUID(user_id))


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_data: PostUpdate,
    session: SessionDep,
    post_id: str,
    user_id: str = Depends(current_user),
):
    return update_user_post(session, UUID(user_id), UUID(post_id), post_data)


@router.delete("/{post_id}")
def delete_post_route(
    session: SessionDep,
    post_id: str,
    user_id: str = Depends(current_user),
):
    return delete_user_post(session, UUID(user_id), UUID(post_id))
