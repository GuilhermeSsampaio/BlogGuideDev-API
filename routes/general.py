from fastapi import APIRouter

router = APIRouter(tags=["general"])

@router.get("/")
def root():
    """Rota principal da API"""
    return {"message": "Bem-vindo à API do BlogGuide!", "version": "1.0.0"}

@router.get("/health")
def health_check():
    """Health check da API"""
    return {"status": "OK", "message": "API funcionando corretamente"}