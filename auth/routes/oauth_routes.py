from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
from config.db import SessionDep
from config.settings import GOOGLE_REDIRECT_URI, FRONTEND_URL
from auth.services.oauth_service import get_or_create_oauth_user
from auth.security.tokens import create_access_token, create_refresh_token
from auth.schemas.token_schema import TokenResponse
from auth.security.google_setup import oauth

# Define o prefixo. As URLs finais serão /auth/google e /auth/google/callback
router = APIRouter(prefix="/auth/google", tags=["OAuth"])


@router.get("/")
async def google_login(request: Request):
    """Redireciona o usuário para a página de login do Google"""

    print(f"Tentando login Google com Redirect URI: '{GOOGLE_REDIRECT_URI}'")

    if not GOOGLE_REDIRECT_URI:
        raise HTTPException(
            status_code=500, detail="Configuração de REDIRECT_URI está vazia."
        )

    return await oauth.google.authorize_redirect(request, GOOGLE_REDIRECT_URI)


@router.get("/callback")
async def google_callback(request: Request, session: SessionDep):
    """Recebe o retorno do Google, cria o usuário se necessário e redireciona para o frontend com o token"""

    # Previne loop: se já tem error na query, redireciona direto para o frontend
    error_param = request.query_params.get("error")
    if error_param:
        params = urlencode({"error": error_param})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        print(f"Erro OAuth: {e}")
        params = urlencode({"error": f"Erro na autenticação: {str(e)}"})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    user_info = token.get("userinfo")
    if not user_info:
        params = urlencode({"error": "Não foi possível obter dados do Google"})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    email = user_info.get("email")
    provider_sub = user_info.get("sub")  # ID único do usuário no Google

    if not email:
        params = urlencode({"error": "Email não retornado pelo Google"})
        return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")

    # Lógica de negócio via Service
    user = get_or_create_oauth_user(session, email, "google", provider_sub)

    # Gera o token da API (interno)
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    # Redireciona para o frontend com os tokens na URL
    params = urlencode({"access_token": access_token, "refresh_token": refresh_token})
    return RedirectResponse(url=f"{FRONTEND_URL}/auth/google/callback?{params}")
