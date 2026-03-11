from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from uuid import UUID

from auth.security.dependencies import current_user, require_role
from models.blogguide_user import TipoPerfil
from config.db import SessionDep
from helpers.profile_helpers import get_profile_or_404

from schemas.vaga_schema import VagaCreate, VagaUpdate, VagaResponse, VagaRecrutadorResponse
from repository.crud import (
    list_vagas_ativas,
    get_vaga_by_id,
    list_vagas_by_recrutador,
    create_vaga,
    update_vaga as update_vaga_db,
    delete_vaga,
)

router = APIRouter()


def _to_response(vaga) -> VagaResponse:
    """Converte Vaga model em VagaResponse."""
    return VagaResponse(
        id=vaga.id,
        titulo=vaga.titulo,
        descricao=vaga.descricao,
        empresa=vaga.empresa,
        localidade=vaga.localidade,
        tipo_contrato=vaga.tipo_contrato,
        link=vaga.link,
        ativa=vaga.ativa,
        data_criacao=vaga.data_criacao,
        recrutador=VagaRecrutadorResponse(
            username=vaga.recrutador.user.username,
            empresa=vaga.recrutador.empresa,
            profile_picture=vaga.recrutador.profile_picture,
        ),
    )


# ── Públicas ──────────────────────────────────────


@router.get("/", response_model=List[VagaResponse])
def listar_vagas(session: SessionDep):
    """Lista todas as vagas ativas (público)."""
    vagas = list_vagas_ativas(session)
    return [_to_response(v) for v in vagas]


@router.get("/{vaga_id}", response_model=VagaResponse)
def detalhe_vaga(vaga_id: UUID, session: SessionDep):
    """Detalhe de uma vaga (público)."""
    vaga = get_vaga_by_id(session, vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    return _to_response(vaga)


# ── Recrutador ──────────────────────────────────────


@router.get("/minhas/list", response_model=List[VagaResponse])
def minhas_vagas(
    session: SessionDep,
    user_id: str = Depends(require_role(TipoPerfil.recrutador)),
):
    """Lista vagas do recrutador autenticado."""
    profile = get_profile_or_404(session, UUID(user_id))
    vagas = list_vagas_by_recrutador(session, profile.id)
    return [_to_response(v) for v in vagas]


@router.post("/", response_model=VagaResponse, status_code=status.HTTP_201_CREATED)
def criar_vaga(
    vaga_data: VagaCreate,
    session: SessionDep,
    user_id: str = Depends(require_role(TipoPerfil.recrutador)),
):
    """Cria uma nova vaga (apenas recrutador)."""
    profile = get_profile_or_404(session, UUID(user_id))
    vaga = create_vaga(session, profile.id, vaga_data)
    return _to_response(vaga)


@router.put("/{vaga_id}", response_model=VagaResponse)
def atualizar_vaga(
    vaga_id: UUID,
    vaga_data: VagaUpdate,
    session: SessionDep,
    user_id: str = Depends(require_role(TipoPerfil.recrutador, TipoPerfil.admin)),
):
    """Atualiza uma vaga (apenas o dono ou admin)."""
    profile = get_profile_or_404(session, UUID(user_id))
    vaga = get_vaga_by_id(session, vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    if vaga.recrutador_id != profile.id and profile.tipo_perfil != TipoPerfil.admin:
        raise HTTPException(status_code=403, detail="Sem permissão")

    if vaga_data.titulo is not None:
        vaga.titulo = vaga_data.titulo
    if vaga_data.descricao is not None:
        vaga.descricao = vaga_data.descricao
    if vaga_data.empresa is not None:
        vaga.empresa = vaga_data.empresa
    if vaga_data.localidade is not None:
        vaga.localidade = vaga_data.localidade
    if vaga_data.tipo_contrato is not None:
        vaga.tipo_contrato = vaga_data.tipo_contrato
    if vaga_data.link is not None:
        vaga.link = vaga_data.link
    if vaga_data.ativa is not None:
        vaga.ativa = vaga_data.ativa

    vaga = update_vaga_db(session, vaga)
    return _to_response(vaga)


@router.delete("/{vaga_id}")
def deletar_vaga(
    vaga_id: UUID,
    session: SessionDep,
    user_id: str = Depends(require_role(TipoPerfil.recrutador, TipoPerfil.admin)),
):
    """Deleta uma vaga (apenas o dono ou admin)."""
    profile = get_profile_or_404(session, UUID(user_id))
    vaga = get_vaga_by_id(session, vaga_id)
    if not vaga:
        raise HTTPException(status_code=404, detail="Vaga não encontrada")
    if vaga.recrutador_id != profile.id and profile.tipo_perfil != TipoPerfil.admin:
        raise HTTPException(status_code=403, detail="Sem permissão")

    delete_vaga(session, vaga_id)
    return {"message": "Vaga deletada com sucesso"}
