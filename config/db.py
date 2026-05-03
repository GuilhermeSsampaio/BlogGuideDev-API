import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from config.models import setup_models

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

_connect_args = {}
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    _connect_args = {"check_same_thread": False}
else:
    _connect_args = {"client_encoding": "utf8"}

engine = create_engine(
    DATABASE_URL,
    echo=True,  # true para mostrar as queries no console
    connect_args=_connect_args,
    pool_pre_ping=True,  # verificar se está ativo antes de conectar
)


def create_db_and_tables():
    """
    Cria as tabelas conforme os models definidos.
    O reset automático foi removido para evitar perda de dados.
    """
    # Garante que todos os modelos foram lidos e registrados no metadata
    setup_models()

    # Cria as tabelas baseadas no que foi registrado
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Cria uma sessão de conexão com o banco.
    Usada como dependência das rotas para acesso seguro ao banco.
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
