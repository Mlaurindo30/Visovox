from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from .jwt_handler import decode_jwt_token
from .user_models import UserInDB
from ..i18n import t

# Endereço do endpoint token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), request: Request = None) -> UserInDB:
    """
    Recupera o usuário autenticado a partir do JWT.
    Utiliza i18n para erros.
    """
    lang = request.headers.get("Accept-Language", "en") if request else "en"
    try:
        payload = decode_jwt_token(token)
        # TODO: Recuperar usuário do banco/cache via payload["sub"]
        user = None  # Implementação real irá buscar o usuário
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=t("errors.user_not_found", language=lang),
            )
        return user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=t("errors.invalid_credentials", language=lang),
        ) 