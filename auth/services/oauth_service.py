from sqlmodel import Session, select
from auth.models.user import User
from auth.models.auth_provider import AuthProvider
from auth.repository.crud import get_user_by_email


def get_or_create_oauth_user(
    session: Session, email: str, provider_name: str, provider_user_id: str = None
) -> User:
    """
    Busca usuário pelo email. Se não existir, cria.
    Verifica se o provider (ex: google) existe. Se não, associa.
    """
    user = get_user_by_email(session, email)

    # 1. Se usuário não existir, cria apenas com dados básicos
    if not user:
        user = User(
            username=email,  # Fallback: usa o email como username inicial
            email=email,
            is_active=True,
        )
        session.add(user)
        session.commit()
        session.refresh(user)

    # 2. Verifica se o provider (Google) já está linkado
    statement = select(AuthProvider).where(
        AuthProvider.user_id == user.id, AuthProvider.provider == provider_name
    )
    provider = session.exec(statement).first()

    # 3. Se não estiver linkado, adiciona o provider
    if not provider:
        provider = AuthProvider(
            user_id=user.id, provider=provider_name, provider_user_id=provider_user_id
        )
        session.add(provider)
        session.commit()

    return user
