from sqlalchemy import func
from sqlmodel import Session, select
from auth.models.user import User
from auth.schemas.user_schema import UserResponse


def get_user_by_email(session: Session, email: str) -> UserResponse | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()


def get_user_by_username(session: Session, username: str) -> User | None:
    """Busca um usuário pelo username (case-insensitive)."""
    statement = select(User).where(
        func.lower(User.username) == username.strip().lower()
    )
    return session.exec(statement).first()
