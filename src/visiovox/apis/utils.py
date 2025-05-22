# src/visiovox/apis/utils.py

from fastapi import Request
from typing import Any, Optional, Dict
from uuid import uuid4

# from .i18n import t  # Helper de tradução multilíngue, quando implementado

def success_response(
    data: Any,
    message: str = "",
    language: str = "en",
    status_code: int = 200,
) -> Dict[str, Any]:
    """
    Gera uma resposta padrão de sucesso para a API.

    Args:
        data (Any): Dados de retorno.
        message (str, opcional): Mensagem de sucesso.
        language (str, opcional): Idioma da resposta.
        status_code (int, opcional): Código HTTP.

    Returns:
        dict: Dicionário padronizado para resposta.
    """
    return {
        "status": "success",
        "message": message,  # TODO: t(message, language) se multilíngue
        "data": data,
        "code": status_code,
        "request_id": str(uuid4()),
    }

def error_response(
    error_code: str,
    message: str = "",
    language: str = "en",
    status_code: int = 400,
    details: Any = None,
) -> Dict[str, Any]:
    """
    Gera uma resposta padronizada de erro para a API.

    Args:
        error_code (str): Código do erro (internacionalizável).
        message (str, opcional): Mensagem do erro.
        language (str, opcional): Idioma da resposta.
        status_code (int, opcional): Código HTTP.
        details (Any, opcional): Dados adicionais sobre o erro.

    Returns:
        dict: Dicionário padronizado para resposta de erro.
    """
    return {
        "status": "error",
        "error_code": error_code,
        "message": message,  # TODO: t(message, language)
        "details": details,
        "code": status_code,
        "request_id": str(uuid4()),
    }

def get_language_from_request(request: Request) -> str:
    """
    Extrai o idioma preferencial da requisição, baseado no header 'Accept-Language'
    ou outro critério (ex: query param, perfil do usuário).

    Args:
        request (Request): Objeto da requisição FastAPI.

    Returns:
        str: Código do idioma ("en", "pt", etc.)
    """
    accept_language = request.headers.get("accept-language", "")
    # TODO: Lógica mais robusta, fallback, integração com i18n
    if accept_language:
        return accept_language.split(",")[0].lower()
    return "en"

def parse_bool(value: Any) -> bool:
    """
    Converte valores diversos em booleano, para parsing de query/body.

    Args:
        value (Any): Valor a ser convertido.

    Returns:
        bool: Valor convertido.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ("true", "1", "yes", "y", "sim")
    return bool(value)

def parse_list(value: Any) -> list:
    """
    Converte valor em lista, útil para query/body params múltiplos.

    Args:
        value (Any): Valor a ser convertido.

    Returns:
        list: Lista resultante.
    """
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    if value is None:
        return []
    return [value]

# TODO: Adicionar helpers para logs, validação de paths, UUIDs seguros, etc. conforme necessidade
