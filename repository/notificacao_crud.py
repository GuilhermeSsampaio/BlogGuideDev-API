from typing import List
from uuid import UUID

from sqlmodel import Session, select

from models.notificacao import Notificacao


def create_notificacao(
    session: Session,
    destinatario_id: UUID,
    tipo: str,
    referencia_id: UUID,
    tipo_referencia: str,
    mensagem: str,
    ator_id: UUID | None = None,
) -> Notificacao:
    notificacao = Notificacao(
        destinatario_id=destinatario_id,
        ator_id=ator_id,
        tipo=tipo,
        referencia_id=referencia_id,
        tipo_referencia=tipo_referencia,
        mensagem=mensagem,
    )
    session.add(notificacao)
    session.commit()
    session.refresh(notificacao)
    return notificacao


def list_notificacoes_usuario(session: Session, destinatario_id: UUID, limit: int = 50) -> List[Notificacao]:
    return session.exec(
        select(Notificacao)
        .where(Notificacao.destinatario_id == destinatario_id)
        .order_by(Notificacao.data_criacao.desc())
        .limit(limit)
    ).all()


def mark_notificacao_as_read(session: Session, notificacao_id: UUID, destinatario_id: UUID) -> Notificacao | None:
    notificacao = session.exec(
        select(Notificacao).where(
            Notificacao.id == notificacao_id,
            Notificacao.destinatario_id == destinatario_id,
        )
    ).first()

    if not notificacao:
        return None

    notificacao.lida = True
    session.add(notificacao)
    session.commit()
    session.refresh(notificacao)
    return notificacao


def count_unread_notificacoes(session: Session, destinatario_id: UUID) -> int:
    notificacoes = session.exec(
        select(Notificacao.id).where(
            Notificacao.destinatario_id == destinatario_id,
            Notificacao.lida == False,
        )
    ).all()
    return len(notificacoes)
