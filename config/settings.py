import os

API_TITLE = "API do BlogGuide - Guilherme & Pedro"
API_VERSION = "2.0"

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-dev")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

GOOGLE_CLIENT_ID = os.getenv("CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv(
    "REDIRECT_URI", "http://localhost:8000/auth/google/callback"
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
HTTPS_ONLY = os.getenv("HTTPS_ONLY", "false").strip().lower() == "true"
