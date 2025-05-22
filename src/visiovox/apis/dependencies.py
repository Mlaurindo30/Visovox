# src/visiovox/apis/dependencies.py

from fastapi import Depends, Request, HTTPException, status
from typing import Optional, Any
# from .auth.jwt_handler import decode_jwt_token
# from .auth.user_models import User
# from .config import settings

def get_settings() -> Any:
    """
    Retorna as configurações globais da API.
    Permite uso como dependência para acesso tipado/configs seguras.
    """
    # TODO: Importar settings da config ou ConfigManager do core
    # from .config import settings
    # return settings
    pass

def get_i18n_language(request: Request) -> str:
    """
    Obtém o idioma corrente da request, usado em respostas multilíngues.
    Pode ser extendido para analisar header, param, cookie, ou perfil autenticado.

    Args:
        request (Request): Requisição FastAPI.

    Returns:
        str: Código do idioma.
    """
    # Exemplo: integração com i18n middleware ou contexto global
    return getattr(request.state, "language", "en")

def get_current_user(request: Request) -> Any:
    """
    Recupera o usuário autenticado a partir do JWT/OAuth2 no header Authorization.

    Args:
        request (Request): Requisição FastAPI.

    Returns:
        User: Instância do usuário autenticado.

    Raises:
        HTTPException: 401 se não autenticado ou token inválido.
    """
    # Exemplo de extração de token (pode ser via OAuth2PasswordBearer)
    # token = request.headers.get("authorization", "").replace("Bearer ", "")
    # if not token:
    #     raise HTTPException(status_code=401, detail="Not authenticated")
    # try:
    #     payload = decode_jwt_token(token, settings.jwt_secret.get_secret_value(), settings.jwt_algorithm)
    #     user = User(**payload)
    #     return user
    # except Exception:
    #     raise HTTPException(status_code=401, detail="Invalid token")
    pass

def get_active_user(current_user: Any = Depends(get_current_user)) -> Any:
    """
    Verifica se o usuário autenticado está ativo.

    Args:
        current_user (User): Usuário autenticado.

    Returns:
        User: Usuário autenticado e ativo.

    Raises:
        HTTPException: 403 se usuário estiver inativo ou banido.
    """
    # if not current_user.is_active:
    #     raise HTTPException(status_code=403, detail="Inactive user")
    # return current_user
    pass

# Dependências para outros recursos globais (orchestrator, celery, etc.) podem ser adicionadas aqui:
# def get_orchestrator() -> Orchestrator:
#     ...

# def get_celery_app() -> Celery:
#     ...

# Exemplo de uso em routers/endpoints:
# from .dependencies import get_current_user, get_i18n_language
# @router.get("/me")
# async def get_profile(user = Depends(get_current_user), lang = Depends(get_i18n_language)):
#     ...

# Notas e Recomendações
# Use sempre que possível dependências explicitamente tipadas, pois facilita testes (injetar mocks/fakes) e melhora documentação automática da API.
# A dependência get_current_user pode ser estendida para múltiplas estratégias de autenticação (JWT, OAuth2, API Key).
# get_i18n_language pode evoluir para integrar preferências do usuário autenticado.
# Dependências para orchestrator, celery, db, etc., facilitam desacoplamento e são importantes para integração de tasks e pipelines.
# Modularize as dependências por domínio se necessário (ex: permissões avançadas, recursos de background, etc.). 