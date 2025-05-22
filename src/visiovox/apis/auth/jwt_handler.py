from datetime import timedelta
from typing import Any, Dict, List
from .user_models import UserInDB
from ..core.config_manager import ConfigManager

def create_jwt_token(user: UserInDB, scopes: List[str], expires_delta: timedelta) -> str:
    """
    Gera um JWT de acesso.
    """
    # TODO: Implementar geração de JWT (PyJWT), claims, expiração, assinatura.
    pass

def decode_jwt_token(token: str) -> Dict[str, Any]:
    """
    Decodifica e valida o JWT recebido.
    """
    # TODO: Decodificar JWT, validar claims, verificar expiração.
    pass

def refresh_jwt_token(token: str) -> str:
    """
    Renova um JWT válido, retornando um novo token.
    """
    # TODO: Validar token antigo e gerar novo token.
    pass

def blacklist_token(token: str) -> None:
    """
    Coloca um token na blacklist (invalidando antes do expirar).
    """
    # TODO: Registrar token como inválido (ex: Redis/set em memória)
    pass 