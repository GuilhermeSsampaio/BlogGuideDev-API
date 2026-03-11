from typing import List, Optional
from uuid import UUID
from sqlmodel import select, Session
from sqlalchemy.orm import joinedload

from models.blogguide_user import BlogguideUser
from models.post import Post
from models.forum import Forum
from models.comentario import Comentario
from models.curtida import Curtida
from models.vaga import Vaga
from auth.models.user import User
from auth.models.auth_provider import AuthProvider
from sqlalchemy import func


def list_blogguide_users(session: Session) -> List[BlogguideUser]:
    return session.exec(select(BlogguideUser).options(joinedload(BlogguideUser.user))).all()


def get_blogguide_user_by_user_id(
    session: Session, user_uuid: UUID
) -> Optional[BlogguideUser]:
    """Busca perfil Blogguide pelo user_id (da tabela User). Retorna None se não existir."""
    return session.exec(
        select(BlogguideUser)
        .options(joinedload(BlogguideUser.user))
        .where(BlogguideUser.user_id == user_uuid)
    ).first()


def create_blogguide_user(session: Session, user_uuid: UUID, tipo_perfil: str = "user") -> BlogguideUser:
    """Cria um novo perfil Blogguide vinculado ao user_id."""
    profile = BlogguideUser(user_id=user_uuid, tipo_perfil=tipo_perfil, verified=False)
    session.add(profile)
    session.commit()
    session.refresh(profile)
    # Recarrega com relationship
    return session.exec(
        select(BlogguideUser)
        .options(joinedload(BlogguideUser.user))
        .where(BlogguideUser.id == profile.id)
    ).first()


def update_blogguide_user(session: Session, profile: BlogguideUser) -> BlogguideUser:
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return profile


def create_post(session: Session, blogguide_user_id: UUID, post_data) -> Post:
    """Cria um novo post."""
    post = Post(
        blogguide_user_id=blogguide_user_id,
        title=post_data.title,
        content=post_data.content,
        excerpt=post_data.excerpt,
        image_url=post_data.image_url,
        published=post_data.published,
    )
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def get_post_by_id(session: Session, post_id: UUID) -> Optional[Post]:
    """Busca um post pelo ID."""
    return session.exec(select(Post).where(Post.id == post_id)).first()


def get_user_posts(session: Session, user_id: UUID) -> List[Post]:
    """Busca todos os posts de um usuário."""
    return session.exec(
        select(Post)
        .where(Post.blogguide_user_id == user_id)
    ).all()


def update_post(session: Session, post: Post) -> Post:
    """Atualiza um post."""
    session.add(post)
    session.commit()
    session.refresh(post)
    return post


def delete_post(session: Session, post_id: UUID) -> bool:
    """Deleta um post. Retorna True se foi deletado, False se não encontrou."""
    post = get_post_by_id(session, post_id)
    if post:
        session.delete(post)
        session.commit()
        return True
    return False


def list_published_posts(session: Session) -> List[Post]:
    """Lista todos os posts publicados, com dados do autor."""
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .where(Post.published == True)
        .order_by(Post.created_at.desc())
    ).all()


def get_published_post_by_id(session: Session, post_id: UUID) -> Optional[Post]:
    """Busca um post publicado pelo ID, com dados do autor."""
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .where(Post.id == post_id, Post.published == True)
    ).first()


# ── Forum ────────────────────────────────────────────────


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


# ── Comentários ────────────────────────────────────────────────


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


# ── Curtidas ─────────────────────────────────────────────────


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


# ── Admin ──────────────────────────────────────────────────


def list_all_posts(session: Session) -> List[Post]:
    """Lista todos os posts (publicados e rascunhos) com dados do autor."""
    return session.exec(
        select(Post)
        .options(joinedload(Post.blogguide_user).joinedload(BlogguideUser.user))
        .order_by(Post.created_at.desc())
    ).all()


def admin_delete_post(session: Session, post_id: UUID) -> bool:
    """Admin: deleta qualquer post pelo ID."""
    post = get_post_by_id(session, post_id)
    if post:
        session.delete(post)
        session.commit()
        return True
    return False


def update_user_role(session: Session, profile_id: UUID, new_role: str) -> Optional[BlogguideUser]:
    """Atualiza o tipo_perfil de um usuário."""
    profile = session.get(BlogguideUser, profile_id)
    if not profile:
        return None
    profile.tipo_perfil = new_role
    session.add(profile)
    session.commit()
    session.refresh(profile)
    return session.exec(
        select(BlogguideUser)
        .options(joinedload(BlogguideUser.user))
        .where(BlogguideUser.id == profile.id)
    ).first()


def admin_delete_user(session: Session, profile_id: UUID) -> bool:
    """Admin: deleta um perfil blogguide e o user base associado."""
    profile = session.get(BlogguideUser, profile_id)
    if not profile:
        return False
    user = session.get(User, profile.user_id)

    # Deletar posts do perfil
    posts = session.exec(select(Post).where(Post.blogguide_user_id == profile.id)).all()
    for post in posts:
        session.delete(post)

    # Deletar forum topics
    topics = session.exec(select(Forum).where(Forum.autor_id == profile.id)).all()
    for topic in topics:
        session.delete(topic)

    # Deletar comentários
    comentarios = session.exec(select(Comentario).where(Comentario.autor_id == profile.id)).all()
    for c in comentarios:
        session.delete(c)

    # Deletar curtidas
    curtidas = session.exec(select(Curtida).where(Curtida.usuario_id == profile.id)).all()
    for c in curtidas:
        session.delete(c)

    # Deletar auth providers
    providers = session.exec(select(AuthProvider).where(AuthProvider.user_id == profile.user_id)).all()
    for p in providers:
        session.delete(p)

    session.delete(profile)
    if user:
        session.delete(user)

    session.commit()
    return True


def get_admin_stats(session: Session) -> dict:
    """Retorna estatísticas gerais do sistema."""
    total_users = session.exec(select(func.count(BlogguideUser.id))).one()
    total_posts = session.exec(select(func.count(Post.id))).one()
    published_posts = session.exec(
        select(func.count(Post.id)).where(Post.published == True)
    ).one()
    total_topics = session.exec(select(func.count(Forum.id))).one()
    total_comentarios = session.exec(select(func.count(Comentario.id))).one()
    total_curtidas = session.exec(select(func.count(Curtida.id))).one()
    return {
        "total_users": total_users,
        "total_posts": total_posts,
        "published_posts": published_posts,
        "draft_posts": total_posts - published_posts,
        "total_topics": total_topics,
        "total_comentarios": total_comentarios,
        "total_curtidas": total_curtidas,
    }


# ── Vagas ──────────────────────────────────────────────────


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


# ── Pesquisa ──────────────────────────────────────────────


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
