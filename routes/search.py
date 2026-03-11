from fastapi import APIRouter, Query

from config.db import SessionDep
from repository.crud import search_posts, search_forum, search_vagas
from schemas.post_schema import PostAuthorResponse

router = APIRouter()


@router.get("/")
def search(
    q: str = Query(..., min_length=1, max_length=200),
    session: SessionDep = None,
):
    """Pesquisa global em posts, fórum e vagas (rota pública)."""
    posts = search_posts(session, q)
    topics = search_forum(session, q)
    vagas = search_vagas(session, q)

    return {
        "posts": [
            {
                "id": str(p.id),
                "title": p.title,
                "excerpt": p.excerpt,
                "image_url": p.image_url,
                "created_at": p.created_at.isoformat(),
                "author": p.blogguide_user.user.username if p.blogguide_user and p.blogguide_user.user else "Anônimo",
            }
            for p in posts
        ],
        "forum": [
            {
                "id": str(t.id),
                "titulo": t.titulo,
                "tipo": t.tipo,
                "data_criacao": t.data_criacao.isoformat(),
                "autor": t.autor.user.username if t.autor and t.autor.user else "Anônimo",
            }
            for t in topics
        ],
        "vagas": [
            {
                "id": str(v.id),
                "titulo": v.titulo,
                "empresa": v.empresa,
                "localidade": v.localidade,
                "tipo_contrato": v.tipo_contrato,
                "data_criacao": v.data_criacao.isoformat(),
                "recrutador": v.recrutador.user.username if v.recrutador and v.recrutador.user else "Anônimo",
            }
            for v in vagas
        ],
    }
