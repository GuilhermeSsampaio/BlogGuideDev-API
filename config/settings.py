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

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_DIR = os.getenv("UPLOAD_DIR", os.path.join(BASE_DIR, "uploads"))
PROFILE_UPLOAD_DIR = os.path.join(UPLOAD_DIR, "avatars")
MAX_AVATAR_SIZE_MB = int(os.getenv("MAX_AVATAR_SIZE_MB", "5"))
ALLOWED_AVATAR_EXTS = {".png", ".jpg", ".jpeg", ".webp"}
