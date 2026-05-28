from typing import List
from fastapi import Depends, APIRouter, UploadFile, File, Form, Header, HTTPException
from uuid import UUID

from auth.schemas.auth_schema import UserLogin, UserRegister
from auth.schemas.token_schema import TokenResponse
from auth.security.dependencies import current_user, require_role
from models.blogguide_user import TipoPerfil
from config.db import SessionDep
from config.settings import VAPID_PRIVATE_KEY, VAPID_PUBLIC_KEY, VAPID_SUBJECT
from helpers.profile_helpers import get_profile_or_404

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
    get_public_profile,
    get_user_stats,
    list_all_blogguide_users,
    list_public_profiles,
    register_blogguide_user,
    save_post_for_user,
    list_user_posts,
    get_user_post_by_id,
    update_user_post,
    delete_user_post,
)
from repository.crud import (
    list_notificacoes_usuario,
    count_unread_notificacoes,
    mark_notificacao_as_read,
    mark_all_notificacoes_as_read,
    remove_push_subscription,
    upsert_push_subscription,
)
from schemas.notificacao_schema import (
    NotificacaoListResponse,
    NotificacaoReadResponse,
    NotificacaoResponse,
)
from schemas.push_schema import (
    PushPublicKeyResponse,
    PushSubscribeResponse,
    PushSubscriptionIn,
    PushUnsubscribeRequest,
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


@router.get("/public", response_model=List[BlogguideUserResponse])
def get_public_users(session: SessionDep):
    return list_public_profiles(session)


@router.get("/public/{username}", response_model=BlogguideUserResponse)
def get_public_user_profile(username: str, session: SessionDep):
    return get_public_profile(session, username)


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
    username: str | None = Form(None),
    nome_completo: str | None = Form(None),
    bio: str | None = Form(None),
    github: str | None = Form(None),
    linkedin: str | None = Form(None),
    is_public: bool | None = Form(None),
    avatar: UploadFile | None = File(None),
):
    # Endpoint dedicado a multipart/form-data para avatar.
    return await edit_profile_with_avatar(
        session,
        UUID(user_id),
        username,
        nome_completo,
        bio,
        github,
        linkedin,
        is_public,
        avatar,
    )


@router.get("/notificacoes", response_model=NotificacaoListResponse)
def get_notificacoes(
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    profile = get_my_profile(session, UUID(user_id))
    items = list_notificacoes_usuario(session, profile.id)
    unread = count_unread_notificacoes(session, profile.id)
    return NotificacaoListResponse(
        unread_count=unread,
        items=[NotificacaoResponse.model_validate(item) for item in items],
    )


@router.put("/notificacoes/read-all", response_model=dict)
def read_all_notificacoes(
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    profile = get_my_profile(session, UUID(user_id))
    mark_all_notificacoes_as_read(session, profile.id)
    return {"message": "Todas as notificações marcadas como lidas."}


@router.put("/notificacoes/{notificacao_id}/read", response_model=NotificacaoReadResponse)
def read_notificacao(
    notificacao_id: UUID,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    profile = get_my_profile(session, UUID(user_id))
    notificacao = mark_notificacao_as_read(session, notificacao_id, profile.id)
    if not notificacao:
        return NotificacaoReadResponse(success=False, notificacao=None)
    return NotificacaoReadResponse(
        success=True,
        notificacao=NotificacaoResponse.model_validate(notificacao),
    )


@router.get("/push/public-key", response_model=PushPublicKeyResponse)
def get_push_public_key(user_id: str = Depends(current_user)):
    if not (VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY and VAPID_SUBJECT):
        raise HTTPException(status_code=503, detail="Notificacoes push nao configuradas")
    return PushPublicKeyResponse(public_key=VAPID_PUBLIC_KEY)


@router.post("/push/subscribe", response_model=PushSubscribeResponse)
def subscribe_push(
    payload: PushSubscriptionIn,
    session: SessionDep,
    user_id: str = Depends(current_user),
    user_agent: str | None = Header(default=None),
):
    if not (VAPID_PUBLIC_KEY and VAPID_PRIVATE_KEY and VAPID_SUBJECT):
        raise HTTPException(status_code=503, detail="Notificacoes push nao configuradas")

    profile = get_profile_or_404(session, UUID(user_id))
    upsert_push_subscription(
        session,
        user_id=profile.id,
        endpoint=payload.endpoint,
        p256dh=payload.keys.p256dh,
        auth=payload.keys.auth,
        expiration_time=payload.expiration_time,
        user_agent=user_agent,
    )
    return PushSubscribeResponse(success=True)


@router.post("/push/unsubscribe", response_model=PushSubscribeResponse)
def unsubscribe_push(
    payload: PushUnsubscribeRequest,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    profile = get_profile_or_404(session, UUID(user_id))
    removed = remove_push_subscription(session, payload.endpoint, profile.id)
    return PushSubscribeResponse(success=removed)


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


@router.get("/my_post/{post_id}", response_model=PostResponse)
def get_my_post(
    session: SessionDep,
    post_id: str,
    user_id: str = Depends(require_role(TipoPerfil.admin)),
):
    return get_user_post_by_id(session, UUID(user_id), UUID(post_id))


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
