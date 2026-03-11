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
    delete_forum_topic,
)
from schemas.forum_schema import (
    ForumCreate,
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
        data_criacao=topic.data_criacao,
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
    return _to_forum_response(topic)


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
