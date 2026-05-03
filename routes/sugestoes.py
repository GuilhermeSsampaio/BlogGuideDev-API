from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException

from auth.security.dependencies import current_user, require_role
from auth.security.tokens import decode_token
from config.db import SessionDep
from models.blogguide_user import TipoPerfil
from models.sugestao import Sugestao
from repository.crud import create_sugestao, list_sugestoes, list_sugestoes_by_user
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

    user_id: UUID | None = None
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization.split(" ", 1)[1]
        payload = decode_token(token)
        if payload and payload.get("sub"):
            user_id = UUID(payload["sub"])

    sugestao = Sugestao(
        user_id=user_id,
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
    items = list_sugestoes_by_user(session, UUID(user_id))
    return [SugestaoResponse.model_validate(item) for item in items]


@router.get("/", response_model=list[SugestaoResponse])
def listar_sugestoes_admin(
    session: SessionDep,
    user_id: str = Depends(require_role(TipoPerfil.admin)),
):
    items = list_sugestoes(session)
    return [SugestaoResponse.model_validate(item) for item in items]
