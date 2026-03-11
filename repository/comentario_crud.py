from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser
from models.comentario import Comentario


def list_comentarios(session: Session, referencia_id: UUID, tipo_referencia: str) -> List[Comentario]:
    """Lista comentários de uma referência (post ou forum)."""
    return session.exec(
        select(Comentario)
        .options(joinedload(Comentario.autor).joinedload(BlogguideUser.user))
        .where(
            Comentario.referencia_id == referencia_id,
            Comentario.tipo_referencia == tipo_referencia,
        )
        .order_by(Comentario.data.asc())
    ).all()


def create_comentario(
    session: Session, autor_id: UUID, referencia_id: UUID, tipo_referencia: str, conteudo: str
) -> Comentario:
    """Cria um comentário."""
    comentario = Comentario(
        conteudo=conteudo,
        autor_id=autor_id,
        referencia_id=referencia_id,
        tipo_referencia=tipo_referencia,
    )
    session.add(comentario)
    session.commit()
    session.refresh(comentario)
    return session.exec(
        select(Comentario)
        .options(joinedload(Comentario.autor).joinedload(BlogguideUser.user))
        .where(Comentario.id == comentario.id)
    ).first()


def delete_comentario(session: Session, comentario_id: UUID) -> bool:
    """Deleta um comentário."""
    comentario = session.get(Comentario, comentario_id)
    if comentario:
        session.delete(comentario)
        session.commit()
        return True
    return False


def get_comentario_by_id(session: Session, comentario_id: UUID) -> Optional[Comentario]:
    """Busca um comentário pelo ID."""
    return session.exec(
        select(Comentario)
        .options(joinedload(Comentario.autor).joinedload(BlogguideUser.user))
        .where(Comentario.id == comentario_id)
    ).first()
