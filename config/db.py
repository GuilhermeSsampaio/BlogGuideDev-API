from math import e
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session
from config.models import setup_models

load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
RESET_DB = os.environ.get("RESET_DB", "False")

engine = create_engine(
    DATABASE_URL,
    echo=True,  # true para mostrar as queries no console
    connect_args={"client_encoding": "utf8"},
    pool_pre_ping=True,  # verificar se está ativo antes de conectar
)


def create_db_and_tables():
    """ "
    Cria as tabelas conforme os models definidos
    Deve ser chamada uma vez ao iniciar o projeto ou atualizar modelos
    """
    # Garante que todos os modelos foram lidos e registrados no metadata
    setup_models()

    should_reset = RESET_DB.strip().lower() == "true"

    if should_reset:
        SQLModel.metadata.drop_all(engine)

    # Cria as tabelas baseadas no que foi registrado
    SQLModel.metadata.create_all(engine)


def get_session():
    """ "
    Cria uma sessão de conexão com o banco
    Usada para trabalhas o crud dentro dos endpoints, deve ser usado
    como dependência das rotas para acessar o banco de forma segura e automática
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
