from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.security.tokens import decode_token

http_bearer = HTTPBearer()


def current_user(credentials: HTTPAuthorizationCredentials = Depends(http_bearer)):
    payload = decode_token(credentials.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )

    return payload["sub"]
