from multiprocessing import process
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from database import create_db_and_tables, get_session
from models.post import Post, PostCreate, PostResponse
from typing import List
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()


app = FastAPI(title="Bloguide API", version="1.0.0")
interface_url = os.getenv("BASE_INTERFACE_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def rota_main():
    return {"Hello": "World"}

@app.post("/new-post", response_model=PostResponse)
def rota_new_post(post: PostCreate, session: Session = Depends(get_session)):
    """Criar um novo post"""
    db_post = Post.from_orm(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@app.get("/posts", response_model=List[PostResponse])
def get_posts(session: Session = Depends(get_session)):
    """Listar todos os posts"""
    statement = select(Post)
    posts = session.exec(statement).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int, session: Session = Depends(get_session)):
    """Obter um post específico"""
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    return post

@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, session: Session = Depends(get_session)):
    """Atualizar um post existente"""
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    db_post.title = post.title
    db_post.content = post.content
    db_post.author = post.author
    db_post.updated_at = datetime.now()
    
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    
    return db_post

@app.delete("/posts/{post_id}", response_model=PostResponse)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    """Deletar um post"""
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post não encontrado")
    
    session.delete(db_post)
    session.commit()
    
    return db_post