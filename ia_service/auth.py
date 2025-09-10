# auth.py
from fastapi import HTTPException, Header, status, Depends
from typing import Optional

# Tokens válidos (em produção trocar por store seguro)
VALID_TOKENS = {
    "secrettoken123",     # token de exemplo
    "reportingtoken456"
}

def get_current_token(authorization: Optional[str] = Header(None)):
    """
    Espera header: Authorization: Bearer <token>
    """
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing Authorization header")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authorization header format. Use: Bearer <token>")
    token = parts[1]
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    # Retornamos o token como "current user" simples
    return token

# Dependency para usar nas rotas:
def require_token(token: str = Depends(get_current_token)):
    return token