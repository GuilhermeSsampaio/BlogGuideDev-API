from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session

from models.blogguide_user import BlogguideUser
from repository.crud import get_blogguide_user_by_user_id
from schemas.blogguide_user_schema import BlogguideUserResponse


def get_profile_or_404(session: Session, user_uuid: UUID) -> BlogguideUser:
    """Busca perfil Blogguide pelo user_id ou lança 404."""
    profile = get_blogguide_user_by_user_id(session, user_uuid)

    if not profile:
        raise HTTPException(status_code=404, detail="Perfil Blogguide não encontrado")

    return profile


def to_blogguide_response(profile: BlogguideUser) -> BlogguideUserResponse:
    """Converte um BlogguideUser (com user carregado) em BlogguideUserResponse."""
    return BlogguideUserResponse(
        id=profile.id,
        user_id=profile.user_id,
        username=profile.user.username,
        email=profile.user.email,
        tipo_perfil=profile.tipo_perfil,
        bio=profile.bio,
        profile_picture=profile.profile_picture,
        empresa=profile.empresa,
        verified=profile.verified,
    )
