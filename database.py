from sqlmodel import create_engine, SQLModel, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# URL do banco de dados - agora configurável
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bloguide.db")

print(f"🔧 Database URL carregada: {DATABASE_URL}")

# Configurações específicas para PostgreSQL
if DATABASE_URL.startswith("postgresql"):
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # Para ver as queries no console
        pool_pre_ping=True,  # Verificar conexões antes de usar
        pool_recycle=300,    # Reciclar conexões a cada 5 minutos
    )
    print("🐘 Configurado para PostgreSQL")
else:
    # SQLite (padrão para desenvolvimento)
    engine = create_engine(DATABASE_URL, echo=True)
    print("📁 Configurado para SQLite")

def create_db_and_tables():
    """Criar banco de dados e tabelas"""
    print(f"Conectando ao banco: {DATABASE_URL}")
    SQLModel.metadata.create_all(engine)
    print("Tabelas criadas com sucesso!")

def get_session() -> Generator[Session, None, None]:
    """Dependency para obter sessão do banco"""
    with Session(engine) as session:
        yield session