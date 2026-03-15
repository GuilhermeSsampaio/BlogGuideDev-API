from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from config.db import SessionDep
from auth.schemas.auth_schema import UserRegister, UserLogin
from auth.schemas.user_schema import UserResponse
from auth.schemas.token_schema import TokenResponse, RefreshTokenRequest
from auth.services.auth_service import create_user, login_user
from auth.security.dependencies import current_user
from auth.security.tokens import create_access_token, create_refresh_token, decode_refresh_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse)
def register(user_data: UserRegister, session: SessionDep):
    try:
        user = create_user(session, user_data)
        return user
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email ou username já cadastrado",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, session: SessionDep):
    from auth.repository.crud import get_user_by_email
    user = get_user_by_email(session, credentials.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não cadastrado, faça seu registro."
        )

    tokens = login_user(session, credentials.email, credentials.password)
    if not tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas"
        )
    return {**tokens, "token_type": "bearer"}


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(body: RefreshTokenRequest):
    """Gera um novo access_token a partir de um refresh_token válido."""
    payload = decode_refresh_token(body.refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido ou expirado",
        )

    user_id = payload.get("sub")
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_refresh_token({"sub": user_id})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@router.get("/protected")
def protected_route(user_id: str = Depends(current_user)):
    return {"message": "rota protegida acessada", "userid": user_id}
