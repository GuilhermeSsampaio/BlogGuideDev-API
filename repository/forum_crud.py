from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser
from models.forum import Forum


def list_forum_topics(session: Session) -> List[Forum]:
    """Lista todos os tópicos do fórum, com dados do autor."""
    return session.exec(
        select(Forum)
        .options(joinedload(Forum.autor).joinedload(BlogguideUser.user))
        .order_by(Forum.data_criacao.desc())
    ).all()


def get_forum_topic_by_id(session: Session, topic_id: UUID) -> Optional[Forum]:
    """Busca um tópico pelo ID, com dados do autor."""
    return session.exec(
        select(Forum)
        .options(joinedload(Forum.autor).joinedload(BlogguideUser.user))
        .where(Forum.id == topic_id)
    ).first()


def create_forum_topic(session: Session, autor_id: UUID, topic_data) -> Forum:
    """Cria um novo tópico no fórum."""
    topic = Forum(
        titulo=topic_data.titulo,
        descricao=topic_data.descricao,
        tipo=topic_data.tipo,
        autor_id=autor_id,
    )
    session.add(topic)
    session.commit()
    session.refresh(topic)
    return session.exec(
        select(Forum)
        .options(joinedload(Forum.autor).joinedload(BlogguideUser.user))
        .where(Forum.id == topic.id)
    ).first()


def delete_forum_topic(session: Session, topic_id: UUID) -> bool:
    """Deleta um tópico do fórum."""
    topic = get_forum_topic_by_id(session, topic_id)
    if topic:
        session.delete(topic)
        session.commit()
        return True
    return False
