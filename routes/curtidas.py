from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from auth.security.dependencies import current_user
from config.db import SessionDep
from helpers.profile_helpers import get_profile_or_404
from repository.crud import toggle_curtida, count_curtidas, get_curtida
from schemas.curtida_schema import CurtidaToggleResponse, CurtidaCountResponse

router = APIRouter()

TIPOS_VALIDOS = ("post", "forum", "comentario", "conteudo")


@router.post("/{tipo_referencia}/{referencia_id}", response_model=CurtidaToggleResponse)
def toggle_like(
    tipo_referencia: str,
    referencia_id: UUID,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Alterna curtida (curtir/descurtir) em post, forum ou comentário."""
    if tipo_referencia not in TIPOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"tipo_referencia deve ser: {', '.join(TIPOS_VALIDOS)}")
    profile = get_profile_or_404(session, UUID(user_id))
    curtido = toggle_curtida(session, profile.id, referencia_id, tipo_referencia)
    total = count_curtidas(session, referencia_id, tipo_referencia)
    return CurtidaToggleResponse(curtido=curtido, total=total)


@router.get("/{tipo_referencia}/{referencia_id}", response_model=CurtidaCountResponse)
def get_likes(
    tipo_referencia: str,
    referencia_id: UUID,
    session: SessionDep,
    user_id: str = None,
):
    """Retorna total de curtidas e se o usuário atual curtiu (rota pública)."""
    if tipo_referencia not in TIPOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"tipo_referencia deve ser: {', '.join(TIPOS_VALIDOS)}")
    total = count_curtidas(session, referencia_id, tipo_referencia)
    return CurtidaCountResponse(total=total, curtido_por_usuario=False)


@router.get("/{tipo_referencia}/{referencia_id}/me", response_model=CurtidaCountResponse)
def get_likes_with_user(
    tipo_referencia: str,
    referencia_id: UUID,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Retorna total de curtidas e se o usuário logado curtiu."""
    if tipo_referencia not in TIPOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"tipo_referencia deve ser: {', '.join(TIPOS_VALIDOS)}")
    profile = get_profile_or_404(session, UUID(user_id))
    total = count_curtidas(session, referencia_id, tipo_referencia)
    curtida = get_curtida(session, profile.id, referencia_id, tipo_referencia)
    return CurtidaCountResponse(total=total, curtido_por_usuario=curtida is not None)
