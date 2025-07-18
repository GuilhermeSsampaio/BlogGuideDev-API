from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from database import get_session
from models.user import User, UserCreate, UserResponse
from models.auth import LoginRequest, LoginResponse, RegisterRequest
from auth.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    verify_token,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=UserResponse)
def register(register_data: RegisterRequest, session: Session = Depends(get_session)):
    """Registrar novo usuário"""
    # Verificar se email já existe
    existing_email = session.exec(select(User).where(User.email == register_data.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já está em uso")
    
    # Verificar se username já existe
    existing_username = session.exec(select(User).where(User.username == register_data.username)).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username já está em uso")
    
    # Criar novo usuário
    hashed_password = get_password_hash(register_data.password)
    db_user = User(
        name=register_data.name,
        username=register_data.username,
        email=register_data.email,
        password_hash=hashed_password,
        bio=register_data.bio
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, session: Session = Depends(get_session)):
    """Login do usuário"""
    # Buscar usuário pelo email
    user = session.exec(select(User).where(User.email == login_data.email)).first()
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )
    
    # Criar token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "avatar_url": user.avatar_url
        }
    )

@router.get("/me", response_model=UserResponse)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """Obter dados do usuário autenticado"""
    token = credentials.credentials
    email = verify_token(token)
    
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return user

@router.post("/logout")
def logout():
    """Logout do usuário"""
    return {"message": "Logout realizado com sucesso"}