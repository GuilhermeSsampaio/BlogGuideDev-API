from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session

from auth.security.tokens import decode_token
from config.db import get_session
from models.blogguide_user import BlogguideUser, TipoPerfil
from repository.crud import get_blogguide_user_by_user_id

http_bearer = HTTPBearer()


def current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    payload = decode_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )

    return payload["sub"]


def require_role(*allowed_roles: TipoPerfil):
    """Dependency factory que exige que o usuário tenha um dos roles permitidos."""
    def role_checker(
        user_id: str = Depends(current_user),
        session: Session = Depends(get_session),
    ):
        from uuid import UUID
        profile = get_blogguide_user_by_user_id(session, UUID(user_id))
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Perfil não encontrado",
            )
        if profile.tipo_perfil not in [r.value for r in allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para esta ação",
            )
        return user_id
    return role_checker
