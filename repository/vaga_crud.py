from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser
from models.vaga import Vaga


def list_vagas_ativas(session: Session) -> List[Vaga]:
    """Lista todas as vagas ativas, com dados do recrutador."""
    return session.exec(
        select(Vaga)
        .options(joinedload(Vaga.recrutador).joinedload(BlogguideUser.user))
        .where(Vaga.ativa == True)
        .order_by(Vaga.data_criacao.desc())
    ).all()


def get_vaga_by_id(session: Session, vaga_id: UUID) -> Optional[Vaga]:
    """Busca uma vaga pelo ID com dados do recrutador."""
    return session.exec(
        select(Vaga)
        .options(joinedload(Vaga.recrutador).joinedload(BlogguideUser.user))
        .where(Vaga.id == vaga_id)
    ).first()


def list_vagas_by_recrutador(session: Session, recrutador_id: UUID) -> List[Vaga]:
    """Lista vagas de um recrutador específico."""
    return session.exec(
        select(Vaga)
        .options(joinedload(Vaga.recrutador).joinedload(BlogguideUser.user))
        .where(Vaga.recrutador_id == recrutador_id)
        .order_by(Vaga.data_criacao.desc())
    ).all()


def create_vaga(session: Session, recrutador_id: UUID, vaga_data) -> Vaga:
    """Cria uma nova vaga."""
    vaga = Vaga(
        titulo=vaga_data.titulo,
        descricao=vaga_data.descricao,
        empresa=vaga_data.empresa,
        localidade=vaga_data.localidade,
        tipo_contrato=vaga_data.tipo_contrato,
        link=vaga_data.link,
        recrutador_id=recrutador_id,
    )
    session.add(vaga)
    session.commit()
    session.refresh(vaga)
    return session.exec(
        select(Vaga)
        .options(joinedload(Vaga.recrutador).joinedload(BlogguideUser.user))
        .where(Vaga.id == vaga.id)
    ).first()


def update_vaga(session: Session, vaga: Vaga) -> Vaga:
    """Atualiza uma vaga."""
    session.add(vaga)
    session.commit()
    session.refresh(vaga)
    return session.exec(
        select(Vaga)
        .options(joinedload(Vaga.recrutador).joinedload(BlogguideUser.user))
        .where(Vaga.id == vaga.id)
    ).first()


def delete_vaga(session: Session, vaga_id: UUID) -> bool:
    """Deleta uma vaga."""
    vaga = session.get(Vaga, vaga_id)
    if vaga:
        session.delete(vaga)
        session.commit()
        return True
    return False
