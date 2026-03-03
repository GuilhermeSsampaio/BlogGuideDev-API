from sqlmodel import Session, select
from auth.models.user import User
from auth.schemas.auth_schema import UserRegister
from auth.security.hashing import hash_password, verify_password
from auth.security.tokens import create_access_token, create_refresh_token
from auth.schemas.user_schema import UserResponse
from auth.models.auth_provider import AuthProvider

from auth.repository.crud import get_user_by_email


def create_user(session: Session, user_data: UserRegister) -> UserResponse:
    hashed_pw = hash_password(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    provider = AuthProvider(
        user_id=user.id, provider="password", password_hash=hashed_pw
    )
    session.add(provider)
    session.commit()

    return user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session, email)

    if not user:
        return None

    statement = select(AuthProvider).where(
        AuthProvider.user_id == user.id, AuthProvider.provider == "password"
    )

    provider = session.exec(statement).first()
    if not provider or not provider.password_hash:
        return None

    if not verify_password(password, provider.password_hash):
        return None

    return user


def login_user(session: Session, email: str, password: str) -> dict | None:
    user = authenticate_user(session, email, password)

    if not user:
        return None

    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "refresh_token": create_refresh_token({"sub": str(user.id)}),
    }
