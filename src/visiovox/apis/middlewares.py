# src/visiovox/apis/middlewares.py

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable, Awaitable, Any
import time

# from .utils import error_response, get_language_from_request
# from .i18n import t

def add_logging_middleware(app: FastAPI) -> None:
    """
    Adiciona middleware de logging à aplicação FastAPI.
    Loga informações de request, response, tempo, erros, etc.
    """
    class LoggingMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
            start_time = time.time()
            # Exemplo de log de request:
            print(f"[REQUEST] {request.method} {request.url}")
            try:
                response = await call_next(request)
            except Exception as e:
                # Exemplo de log de erro:
                print(f"[ERROR] {e}")
                raise
            process_time = (time.time() - start_time) * 1000
            print(f"[RESPONSE] {request.method} {request.url} - {response.status_code} ({process_time:.2f}ms)")
            return response
    app.add_middleware(LoggingMiddleware)

def add_rate_limit_middleware(app: FastAPI, max_requests: int = 100, window_seconds: int = 60) -> None:
    """
    Adiciona middleware de rate limiting à aplicação FastAPI.
    Limita o número de requests por IP em um determinado período.

    Args:
        max_requests (int): Número máximo de requests por IP.
        window_seconds (int): Janela de tempo em segundos.
    """
    from collections import defaultdict
    from starlette.responses import PlainTextResponse

    rate_limits = defaultdict(list)  # {ip: [timestamps]}

    class RateLimitMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
            client_ip = request.client.host
            now = time.time()
            # Limpa timestamps antigos
            timestamps = [t for t in rate_limits[client_ip] if now - t < window_seconds]
            rate_limits[client_ip] = timestamps
            if len(timestamps) >= max_requests:
                # TODO: Internacionalizar mensagem via i18n
                return PlainTextResponse("Too many requests. Please try again later.", status_code=429)
            rate_limits[client_ip].append(now)
            return await call_next(request)
    app.add_middleware(RateLimitMiddleware)

def add_i18n_middleware(app: FastAPI) -> None:
    """
    Adiciona middleware de internacionalização.
    Injeta idioma no contexto de cada request, baseado em Accept-Language ou query param.
    """
    class I18nMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
            # Exemplo de extração de idioma:
            lang = request.headers.get("accept-language", "en").split(",")[0].lower()
            # TODO: Adicionar ao contexto global/contextvars/local/session, conforme estratégia
            request.state.language = lang
            # Exemplo: pode integrar com helper de tradução t(...)
            return await call_next(request)
    app.add_middleware(I18nMiddleware)

def add_error_handling_middleware(app: FastAPI) -> None:
    """
    Adiciona handler global de erros customizados/multilíngues à aplicação.
    """
    @app.exception_handler(Exception)
    async def custom_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        # TODO: Logar o erro, internacionalizar mensagem, diferenciar ambiente (debug/produção)
        # message = t("errors.internal_server_error", language=getattr(request.state, "language", "en"))
        message = "Internal server error"
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error_code": "internal_server_error",
                "message": message,
                "request_id": str(time.time()),
            },
        )

# Exemplo de uso no main.py:
# from .middlewares import add_logging_middleware, add_rate_limit_middleware, add_i18n_middleware, add_error_handling_middleware
# add_logging_middleware(app)
# add_rate_limit_middleware(app)
# add_i18n_middleware(app)
# add_error_handling_middleware(app)

# Notas e Recomendações
# Cada middleware pode ser expandido para logs estruturados (ex: JSON), integração com monitoramento (Sentry, Prometheus), etc.
# Rate limiting aqui é simplificado e deve ser substituído por solução robusta em produção (Redis, external service, etc).
# O middleware de i18n pode usar contextvars para acesso thread-safe ao idioma ao longo da request.
# O handler global de erros pode diferenciar exceções conhecidas e retornar mensagens multilíngues com detalhes.
# Plugue os middlewares no main.py via funções para facilitar testes/mocks e evitar import cíclico. 