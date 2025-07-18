from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from database import create_db_and_tables
from routes import auth, user, post
import os

# Configurar ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = ENVIRONMENT == "development"

app = FastAPI(
    title="Bloguide API",
    description="API para plataforma de blogs",
    version="1.0.0",
    debug=DEBUG
)

# Configurar CORS
if ENVIRONMENT == "production":
    # CORS restrito para produção
     origins = [
        "https://blog-guide-dev-front.vercel.app",  # ✅ SEM barra final
        "https://blog-guide-dev-front.vercel.app/", # ✅ COM barra final (para garantir)
        "https://blogguidedev-api.fly.dev",          # ✅ Sua própria API
    ]
else:
    # CORS amplo para desenvolvimento
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check para Fly.io
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": ENVIRONMENT}

# Incluir rotas
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)

@app.on_event("startup")
def on_startup():
    """Executar na inicialização"""
    try:
        create_db_and_tables()
        print(f"🚀 Aplicação iniciada em modo: {ENVIRONMENT}")
    except Exception as e:
        print(f"❌ Erro na inicialização: {e}")
        raise

@app.exception_handler(404)
def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"detail": "Endpoint não encontrado"}
    )

@app.exception_handler(500)
def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno do servidor"}
    )

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=DEBUG)