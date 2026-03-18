from typing import List, Optional
from sqlmodel import select, Session

from models.conteudo import Conteudo


def get_conteudo_by_slug(session: Session, slug: str) -> Optional[Conteudo]:
    return session.exec(
        select(Conteudo).where(Conteudo.slug == slug)
    ).first()


def list_conteudos(session: Session) -> List[Conteudo]:
    return session.exec(select(Conteudo)).all()


def create_conteudo_if_not_exists(session: Session, slug: str, titulo: str) -> Conteudo:
    existing = get_conteudo_by_slug(session, slug)
    if existing:
        return existing
    conteudo = Conteudo(slug=slug, titulo=titulo)
    session.add(conteudo)
    session.commit()
    session.refresh(conteudo)
    return conteudo
