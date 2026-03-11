from typing import Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy import func

from models.curtida import Curtida


def get_curtida(session: Session, usuario_id: UUID, referencia_id: UUID, tipo_referencia: str) -> Optional[Curtida]:
    """Busca uma curtida específica do usuário."""
    return session.exec(
        select(Curtida).where(
            Curtida.usuario_id == usuario_id,
            Curtida.referencia_id == referencia_id,
            Curtida.tipo_referencia == tipo_referencia,
        )
    ).first()


def toggle_curtida(session: Session, usuario_id: UUID, referencia_id: UUID, tipo_referencia: str) -> bool:
    """Alterna curtida. Retorna True se curtiu, False se descurtiu."""
    existing = get_curtida(session, usuario_id, referencia_id, tipo_referencia)
    if existing:
        session.delete(existing)
        session.commit()
        return False
    else:
        curtida = Curtida(
            usuario_id=usuario_id,
            referencia_id=referencia_id,
            tipo_referencia=tipo_referencia,
        )
        session.add(curtida)
        session.commit()
        return True


def count_curtidas(session: Session, referencia_id: UUID, tipo_referencia: str) -> int:
    """Conta total de curtidas de uma referência."""
    result = session.exec(
        select(func.count(Curtida.id)).where(
            Curtida.referencia_id == referencia_id,
            Curtida.tipo_referencia == tipo_referencia,
        )
    ).one()
    return result
