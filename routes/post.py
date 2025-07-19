from requests import get, session
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models.post import Post, PostCreate, PostResponse
from models.user import User
from typing import List
from datetime import datetime
import json

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=dict)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    """Criar um novo post"""
    try:
        # Log dos dados recebidos
        print(f"Dados recebidos: {post}")
        
        # Converter tags de lista para string JSON se necessário
        tags_str = None
        if post.tags:
            tags_str = json.dumps(post.tags)
        
        # Criar novo post
        db_post = Post(
            title=post.title,
            category=post.category,
            content=post.content,
            author_id=post.author_id,
            image_url=post.image_url,
            tags=tags_str,
            is_published=getattr(post, 'is_published', True)
        )
        
        session.add(db_post)
        session.commit()
        session.refresh(db_post)
        
        # Retornar resposta simples
        return {
            "id": db_post.id,
            "title": db_post.title,
            "category": db_post.category,
            "content": db_post.content,
            "author_id": db_post.author_id,
            "image_url": db_post.image_url,
            "tags": json.loads(db_post.tags) if db_post.tags else [],
            "likes_count": db_post.likes_count,
            "is_published": db_post.is_published,
            "created_at": db_post.created_at.isoformat(),
            "updated_at": db_post.updated_at.isoformat() if db_post.updated_at else None
        }
        
    except Exception as e:
        print(f"Erro ao criar post: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/", response_model=List[dict])
def get_posts(session: Session = Depends(get_session)):
    """Listar todos os posts"""
    try:
        statement = select(Post)
        posts = session.exec(statement).all()
        
        result = []
        for post in posts:
            result.append({
                "id": post.id,
                "title": post.title,
                "category": post.category,
                "content": post.content,
                "author_id": post.author_id,
                "image_url": post.image_url,
                "tags": json.loads(post.tags) if post.tags else [],
                "likes_count": post.likes_count,
                "is_published": post.is_published,
                "created_at": post.created_at.isoformat(),
                "updated_at": post.updated_at.isoformat() if post.updated_at else None
            })
        
        return result
        
    except Exception as e:
        print(f"Erro ao buscar posts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.get("/{post_id}", response_model=dict)
def get_post(post_id: int, session: Session = Depends(get_session)):
    """Obter um post específico"""
    try:
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post não encontrado")
        
        return {
            "id": post.id,
            "title": post.title,
            "category": post.category,
            "content": post.content,
            "author_id": post.author_id,
            "image_url": post.image_url,
            "tags": json.loads(post.tags) if post.tags else [],
            "likes_count": post.likes_count,
            "is_published": post.is_published,
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat() if post.updated_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao buscar post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

@router.delete("/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session)):
    """Deletar um post"""
    try:
        db_post = session.get(Post, post_id)
        if not db_post:
            raise HTTPException(status_code=404, detail="Post não encontrado")
        
        session.delete(db_post)
        session.commit()
        
        return {"message": "Post deletado com sucesso"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao deletar post: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    
@router.get("/{post_id}/author")
def get_post_author(post_id: int, session: Session = Depends(get_session)):
    """Buscar usuário responsável do post"""
    try:
        # Buscar o post
        post = session.get(Post, post_id)
        if not post:
            raise HTTPException(status_code=404, detail="Post não encontrado")
        
        # Buscar o autor do post
        author = session.get(User, post.author_id)
        if not author:
            raise HTTPException(status_code=404, detail="Autor do post não encontrado")
        
        return {
            "id": author.id,
            "name": author.name,
            "username": author.username,
            "email": author.email,
            "created_at": author.created_at.isoformat() if hasattr(author, 'created_at') else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao buscar autor do post: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
    