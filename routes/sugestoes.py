from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException

from auth.security.dependencies import current_user, require_role
from auth.security.tokens import decode_token
from config.db import SessionDep
from models.blogguide_user import TipoPerfil
from models.sugestao import Sugestao
from repository.crud import create_sugestao, list_sugestoes, list_sugestoes_by_user
from repository.crud import get_blogguide_user_by_user_id
from schemas.sugestao_schema import SugestaoCreate, SugestaoResponse

router = APIRouter()


@router.post("/", response_model=SugestaoResponse, status_code=201)
def criar_sugestao(
    data: SugestaoCreate,
    session: SessionDep,
    authorization: str | None = Header(default=None),
):
    if data.tipo not in ("sugestao", "bug"):
        raise HTTPException(status_code=400, detail="tipo deve ser 'sugestao' ou 'bug'")

    # JWT sub contém User.id (tabela auth), mas Sugestao.user_id faz FK
    # para blogguideuser.id. Precisamos resolver o perfil BlogguideUser.
    profile_id: UUID | None = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        payload = decode_token(token)
        if payload and payload.get("sub"):
            auth_user_id = UUID(payload["sub"])
            profile = get_blogguide_user_by_user_id(session, auth_user_id)
            if profile:
                profile_id = profile.id

    sugestao = Sugestao(
        user_id=profile_id,
        tipo=data.tipo,
        titulo=data.titulo,
        descricao=data.descricao,
        email_contato=data.email_contato,
        canal_contato=data.canal_contato,
    )
    created = create_sugestao(session, sugestao)
    return SugestaoResponse.model_validate(created)


@router.get("/minhas", response_model=list[SugestaoResponse])
def minhas_sugestoes(
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    # user_id do current_user é User.id (auth), precisamos do BlogguideUser.id
    profile = get_blogguide_user_by_user_id(session, UUID(user_id))
    if not profile:
        return []
    items = list_sugestoes_by_user(session, profile.id)
    return [SugestaoResponse.model_validate(item) for item in items]


@router.get("/", response_model=list[SugestaoResponse])
def listar_sugestoes_admin(
    session: SessionDep,
    user_id: str = Depends(require_role(TipoPerfil.admin)),
):
    items = list_sugestoes(session)
    return [SugestaoResponse.model_validate(item) for item in items]

