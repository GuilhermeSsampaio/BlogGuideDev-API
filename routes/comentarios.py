from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from auth.security.dependencies import current_user
from config.db import SessionDep
from helpers.profile_helpers import get_profile_or_404
from repository.crud import (
    list_comentarios,
    list_respostas,
    create_comentario,
    create_notificacao,
    delete_comentario,
    get_post_by_id,
    get_forum_topic_by_id,
    get_comentario_by_id,
)
from schemas.comentario_schema import ComentarioCreate, ComentarioResponse, ComentarioAuthorResponse

router = APIRouter()


def _to_comentario_response(c, respostas: list[ComentarioResponse] | None = None) -> ComentarioResponse:
    return ComentarioResponse(
        id=c.id,
        conteudo=c.conteudo,
        data=c.data,
        referencia_id=c.referencia_id,
        tipo_referencia=c.tipo_referencia,
        parent_id=c.parent_id,
        autor=ComentarioAuthorResponse(
            username=c.autor.user.username,
            profile_picture=c.autor.profile_picture,
        ),
        respostas=respostas or [],
    )


@router.get("/{tipo_referencia}/{referencia_id}", response_model=List[ComentarioResponse])
def get_comentarios(tipo_referencia: str, referencia_id: UUID, session: SessionDep):
    """Lista comentários de um post ou tópico do fórum (rota pública)."""
    if tipo_referencia not in ("post", "forum", "conteudo"):
        raise HTTPException(status_code=400, detail="tipo_referencia deve ser 'post', 'forum' ou 'conteudo'")
    comentarios = list_comentarios(session, referencia_id, tipo_referencia)
    result = []
    for comentario in comentarios:
        respostas = list_respostas(session, comentario.id)
        respostas_response = [_to_comentario_response(r) for r in respostas]
        result.append(_to_comentario_response(comentario, respostas_response))
    return result


@router.post("/{tipo_referencia}/{referencia_id}", response_model=ComentarioResponse, status_code=201)
def criar_comentario(
    tipo_referencia: str,
    referencia_id: UUID,
    data: ComentarioCreate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Cria um comentário em um post ou tópico (autenticado)."""
    if tipo_referencia not in ("post", "forum", "conteudo"):
        raise HTTPException(status_code=400, detail="tipo_referencia deve ser 'post', 'forum' ou 'conteudo'")
    profile = get_profile_or_404(session, UUID(user_id))
    comentario = create_comentario(session, profile.id, referencia_id, tipo_referencia, data.conteudo)

    dono_referencia_id = None
    if tipo_referencia == "post":
        post = get_post_by_id(session, referencia_id)
        dono_referencia_id = post.blogguide_user_id if post else None
    elif tipo_referencia == "forum":
        topic = get_forum_topic_by_id(session, referencia_id)
        dono_referencia_id = topic.autor_id if topic else None

    if dono_referencia_id and dono_referencia_id != profile.id:
        create_notificacao(
            session,
            destinatario_id=dono_referencia_id,
            ator_id=profile.id,
            tipo="comentario",
            referencia_id=comentario.id,
            tipo_referencia=tipo_referencia,
            mensagem=f"{profile.user.username} comentou no seu conteúdo.",
        )

    return _to_comentario_response(comentario)


@router.get("/{comentario_id}/respostas", response_model=List[ComentarioResponse])
def get_respostas(comentario_id: UUID, session: SessionDep):
    """Lista respostas de um comentário."""
    comentario = get_comentario_by_id(session, comentario_id)
    if not comentario:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    respostas = list_respostas(session, comentario_id)
    return [_to_comentario_response(r) for r in respostas]


@router.post("/{comentario_id}/resposta", response_model=ComentarioResponse, status_code=201)
def criar_resposta(
    comentario_id: UUID,
    data: ComentarioCreate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Cria uma resposta para um comentário existente (1 nível)."""
    comentario_pai = get_comentario_by_id(session, comentario_id)
    if not comentario_pai:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")

    if comentario_pai.parent_id is not None:
        raise HTTPException(status_code=400, detail="Só é permitido responder comentários de primeiro nível")

    profile = get_profile_or_404(session, UUID(user_id))
    resposta = create_comentario(
        session,
        profile.id,
        comentario_pai.referencia_id,
        comentario_pai.tipo_referencia,
        data.conteudo,
        parent_id=comentario_pai.id,
    )

    if comentario_pai.autor_id != profile.id:
        create_notificacao(
            session,
            destinatario_id=comentario_pai.autor_id,
            ator_id=profile.id,
            tipo="resposta",
            referencia_id=resposta.id,
            tipo_referencia=comentario_pai.tipo_referencia,
            mensagem=f"{profile.user.username} respondeu seu comentário.",
        )

    return _to_comentario_response(resposta)


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
