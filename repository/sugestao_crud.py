from typing import List
from uuid import UUID

from sqlmodel import Session, select

from models.sugestao import Sugestao


def create_sugestao(session: Session, payload: Sugestao) -> Sugestao:
    session.add(payload)
    session.commit()
    session.refresh(payload)
    return payload


def list_sugestoes(session: Session, limit: int = 100) -> List[Sugestao]:
    return session.exec(
        select(Sugestao)
        .order_by(Sugestao.data_criacao.desc())
        .limit(limit)
    ).all()


def list_sugestoes_by_user(session: Session, user_id: UUID, limit: int = 100) -> List[Sugestao]:
    return session.exec(
        select(Sugestao)
        .where(Sugestao.user_id == user_id)
        .order_by(Sugestao.data_criacao.desc())
        .limit(limit)
    ).all()
