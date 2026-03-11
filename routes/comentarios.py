from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from auth.security.dependencies import current_user
from config.db import SessionDep
from helpers.profile_helpers import get_profile_or_404
from repository.crud import (
    list_comentarios,
    create_comentario,
    delete_comentario,
    get_comentario_by_id,
)
from schemas.comentario_schema import ComentarioCreate, ComentarioResponse, ComentarioAuthorResponse

router = APIRouter()


def _to_comentario_response(c) -> ComentarioResponse:
    return ComentarioResponse(
        id=c.id,
        conteudo=c.conteudo,
        data=c.data,
        referencia_id=c.referencia_id,
        tipo_referencia=c.tipo_referencia,
        autor=ComentarioAuthorResponse(
            username=c.autor.user.username,
            profile_picture=c.autor.profile_picture,
        ),
    )


@router.get("/{tipo_referencia}/{referencia_id}", response_model=List[ComentarioResponse])
def get_comentarios(tipo_referencia: str, referencia_id: UUID, session: SessionDep):
    """Lista comentários de um post ou tópico do fórum (rota pública)."""
    if tipo_referencia not in ("post", "forum"):
        raise HTTPException(status_code=400, detail="tipo_referencia deve ser 'post' ou 'forum'")
    comentarios = list_comentarios(session, referencia_id, tipo_referencia)
    return [_to_comentario_response(c) for c in comentarios]


@router.post("/{tipo_referencia}/{referencia_id}", response_model=ComentarioResponse, status_code=201)
def criar_comentario(
    tipo_referencia: str,
    referencia_id: UUID,
    data: ComentarioCreate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Cria um comentário em um post ou tópico (autenticado)."""
    if tipo_referencia not in ("post", "forum"):
        raise HTTPException(status_code=400, detail="tipo_referencia deve ser 'post' ou 'forum'")
    profile = get_profile_or_404(session, UUID(user_id))
    comentario = create_comentario(session, profile.id, referencia_id, tipo_referencia, data.conteudo)
    return _to_comentario_response(comentario)


@router.delete("/{comentario_id}", status_code=200)
def deletar_comentario(
    comentario_id: UUID,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Deleta um comentário (somente o autor ou admin)."""
    profile = get_profile_or_404(session, UUID(user_id))
    comentario = get_comentario_by_id(session, comentario_id)

    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    if comentario.autor_id != profile.id and profile.tipo_perfil != "admin":
        raise HTTPException(status_code=403, detail="Sem permissão para deletar este comentário")

    delete_comentario(session, comentario_id)
    return {"message": "Comentário deletado com sucesso"}
