from sqlmodel import create_engine, SQLModel, Session
from typing import Generator

# URL do banco de dados SQLite
DATABASE_URL = "sqlite:///./bloguide.db"

# Criar engine
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Criar banco de dados e tabelas"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency para obter sessão do banco"""
    with Session(engine) as session:
        yield session