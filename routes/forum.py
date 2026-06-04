from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID

from auth.security.dependencies import current_user
from config.db import SessionDep
from helpers.profile_helpers import get_profile_or_404
from repository.crud import (
    list_forum_topics,
    get_forum_topic_by_id,
    create_forum_topic,
    update_forum_topic,
    delete_forum_topic,
)
from repository.notificacao_crud import notify_admins
from services.push_service import build_push_payload, queue_push_to_admins
from schemas.forum_schema import (
    ForumCreate,
    ForumUpdate,
    ForumResponse,
    ForumAuthorResponse,
)

router = APIRouter()


def _to_forum_response(topic) -> ForumResponse:
    """Converte um Forum (com autor.user carregados) em ForumResponse."""
    return ForumResponse(
        id=topic.id,
        titulo=topic.titulo,
        descricao=topic.descricao,
        tipo=topic.tipo,
        imagem_url=topic.imagem_url,
        tags=topic.tags,
        data_criacao=topic.data_criacao,
        data_atualizacao=topic.data_atualizacao,
        autor=ForumAuthorResponse(
            username=topic.autor.user.username,
            profile_picture=topic.autor.profile_picture,
        ),
    )


@router.get("/", response_model=List[ForumResponse])
def get_all_topics(session: SessionDep):
    """Lista todos os tópicos do fórum (rota pública)."""
    topics = list_forum_topics(session)
    return [_to_forum_response(t) for t in topics]


@router.get("/{topic_id}", response_model=ForumResponse)
def get_topic(topic_id: UUID, session: SessionDep):
    """Retorna um tópico pelo ID (rota pública)."""
    topic = get_forum_topic_by_id(session, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tópico não encontrado",
        )
    return _to_forum_response(topic)


@router.post("/", response_model=ForumResponse, status_code=status.HTTP_201_CREATED)
def create_topic(
    topic_data: ForumCreate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Cria um novo tópico no fórum (qualquer usuário autenticado)."""
    profile = get_profile_or_404(session, UUID(user_id))
    topic = create_forum_topic(session, profile.id, topic_data)
    
    notify_admins(
        session=session,
        tipo="novo_forum",
        referencia_id=topic.id,
        tipo_referencia="forum",
        mensagem=f"Novo tópico criado por {profile.user.username}: {topic.titulo}",
        ator_id=profile.id,
    )

    payload = build_push_payload(
        title="Novo tópico no fórum",
        body=f"{profile.user.username}: {topic.titulo}",
        url=f"/forum/{topic.id}",
        tag=f"forum-{topic.id}",
    )
    queue_push_to_admins(payload, exclude_user_id=profile.id)
    return _to_forum_response(topic)


@router.put("/{topic_id}", response_model=ForumResponse)
def update_topic(
    topic_id: UUID,
    topic_data: ForumUpdate,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Atualiza um tópico no fórum (somente o autor)."""
    profile = get_profile_or_404(session, UUID(user_id))
    topic = get_forum_topic_by_id(session, topic_id)

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tópico não encontrado",
        )

    if topic.autor_id != profile.id and profile.tipo_perfil != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para atualizar este tópico",
        )

    updated_topic = update_forum_topic(session, topic_id, topic_data)
    return _to_forum_response(updated_topic)


@router.delete("/{topic_id}", status_code=status.HTTP_200_OK)
def delete_topic(
    topic_id: UUID,
    session: SessionDep,
    user_id: str = Depends(current_user),
):
    """Deleta um tópico (somente o autor ou admin)."""
    profile = get_profile_or_404(session, UUID(user_id))
    topic = get_forum_topic_by_id(session, topic_id)

    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tópico não encontrado",
        )

    if topic.autor_id != profile.id and profile.tipo_perfil != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para deletar este tópico",
        )

    delete_forum_topic(session, topic_id)
    return {"message": "Tópico deletado com sucesso"}
