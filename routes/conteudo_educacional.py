from typing import List
from fastapi import APIRouter, HTTPException, status

from config.db import SessionDep
from repository.crud import get_conteudo_by_slug, list_conteudos
from schemas.conteudo_schema import ConteudoResponse

router = APIRouter()


@router.get("/", response_model=List[ConteudoResponse])
def get_all_conteudos(session: SessionDep):
    """Lista todos os conteudos educacionais (rota publica)."""
    return list_conteudos(session)


@router.get("/{slug}", response_model=ConteudoResponse)
def get_conteudo_by_slug_route(slug: str, session: SessionDep):
    """Retorna um conteudo educacional pelo slug (rota publica)."""
    conteudo = get_conteudo_by_slug(session, slug)
    if not conteudo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conteudo educacional nao encontrado",
        )
    return conteudo
