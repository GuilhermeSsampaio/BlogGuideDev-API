from models.user import User, UserCreate, UserResponse, UserUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from typing import List
from datetime import datetime

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def get_users(session: Session = Depends(get_session)):
    """Listar todos os usuários"""
    statement = select(User)
    users = session.exec(statement).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    """Obter um usuário específico"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    """Criar um novo usuário"""
    # Verificar se username já existe
    existing_username = session.exec(select(User).where(User.username == user.username)).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username já existe")
    
    # Verificar se email já existe
    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email já existe")
    
    # Criar novo usuário
    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        bio=user.bio,
        github_url=user.github_url,
        linkedin_url=user.linkedin_url,
        avatar_url=user.avatar_url
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, session: Session = Depends(get_session)):
    """Atualizar um usuário existente"""
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Verificar se novo username já existe (se fornecido)
    if user_update.username and user_update.username != db_user.username:
        existing_username = session.exec(select(User).where(User.username == user_update.username)).first()
        if existing_username:
            raise HTTPException(status_code=400, detail="Username já existe")
    
    # Verificar se novo email já existe (se fornecido)
    if user_update.email and user_update.email != db_user.email:
        existing_email = session.exec(select(User).where(User.email == user_update.email)).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email já existe")
    
    # Atualizar apenas os campos fornecidos
    update_data = user_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    # Atualizar timestamp
    db_user.updated_at = datetime.now()
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    """Deletar um usuário"""
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    session.delete(db_user)
    session.commit()
    return db_user

@router.get("/{user_id}/posts")
def get_user_posts(user_id: int, session: Session = Depends(get_session)):
    """Obter todos os posts de um usuário"""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Retornar posts do usuário (relacionamento já definido no modelo)
    return user.posts

@router.get("/{username}/profile")
def get_user_by_username(username: str, session: Session = Depends(get_session)):
    """Obter perfil público do usuário pelo username"""
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Retornar apenas informações públicas
    return {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "bio": user.bio,
        "github_url": user.github_url,
        "linkedin_url": user.linkedin_url,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at,
        "posts_count": len(user.posts)
    }