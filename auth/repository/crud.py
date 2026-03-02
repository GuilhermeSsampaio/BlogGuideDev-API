from sqlmodel import Session, select
from auth.models.user import User
from auth.schemas.user_schema import UserResponse


def get_user_by_email(session: Session, email: str) -> UserResponse | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()
