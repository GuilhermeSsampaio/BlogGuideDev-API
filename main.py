import os
from fastapi import FastAPI
from database import create_db_and_tables
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Importar as rotas
from routes import post, user, general, auth

load_dotenv()

app = FastAPI(
    title="BlogGuide API", 
    version="1.0.0",
    description="API para o sistema de blog BlogGuideDev"
)

# # Configuração do CORS
# interface_url = os.getenv("BASE_INTERFACE_URL", "http://localhost:5173")
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",  # Alternativa local
        "http://localhost:3000",  # Create React App (se usar)
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Incluir as rotas
app.include_router(general.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.on_event("startup")
def on_startup():
    """Evento executado na inicialização da aplicação"""
    create_db_and_tables()