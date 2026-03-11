from typing import List
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser
from models.post import Post
from models.forum import Forum
from models.vaga import Vaga


def search_posts(session: Session, query: str) -> List[Post]:
    """Busca posts publicados por título ou conteúdo."""
    pattern = f"%{query}%"
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .where(
            Post.published == True,
            (Post.title.ilike(pattern)) | (Post.content.ilike(pattern)) | (Post.excerpt.ilike(pattern)),
        )
        .order_by(Post.created_at.desc())
    ).all()


def search_forum(session: Session, query: str) -> List[Forum]:
    """Busca tópicos do fórum por título ou descrição."""
    pattern = f"%{query}%"
    return session.exec(
        select(Forum)
        .options(joinedload(Forum.autor).joinedload(BlogguideUser.user))
        .where(
            (Forum.titulo.ilike(pattern)) | (Forum.descricao.ilike(pattern)),
        )
        .order_by(Forum.data_criacao.desc())
    ).all()


def search_vagas(session: Session, query: str) -> List[Vaga]:
    """Busca vagas ativas por título, empresa ou descrição."""
    pattern = f"%{query}%"
    return session.exec(
        select(Vaga)
        .options(joinedload(Vaga.recrutador).joinedload(BlogguideUser.user))
        .where(
            Vaga.ativa == True,
            (Vaga.titulo.ilike(pattern)) | (Vaga.empresa.ilike(pattern)) | (Vaga.descricao.ilike(pattern)),
        )
        .order_by(Vaga.data_criacao.desc())
    ).all()
