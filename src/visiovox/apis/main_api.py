# src/visiovox/apis/main.py

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Any

# Routers (Importe apenas os que já existem para evitar erros de import cíclico)
# from .routers.media_ingestion_router import router as media_router
# from .routers.scene_analysis_router import router as scene_router
# from .routers.facial_processing_router import router as face_router
# from .routers.voice_processing_router import router as voice_router
# ... (demais routers)

# Middlewares, dependencies, i18n, auth (imports conforme módulos forem implementados)
# from .middlewares import add_logging_middleware, add_rate_limit_middleware, add_i18n_middleware
# from .dependencies import get_i18n, get_current_user
# from .i18n import t

# Config (pode usar ConfigManager do core ou Pydantic Settings)
# from .config import settings

# Celery app/task integration (imports conforme implementação)
# from .celery_tasks import ...

# --- FastAPI App Instance ---

app = FastAPI(
    title="VisioVox Fusion API",
    description="API Multimodal para manipulação facial e vocal com IA. "
                "Endpoints RESTful, WebSocket, tarefas assíncronas e suporte multilíngue.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# --- Middlewares Globais ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Defina origens adequadas em produção!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Adicionar middlewares customizados: logging, rate limit, i18n, error handling
# add_logging_middleware(app)
# add_rate_limit_middleware(app)
# add_i18n_middleware(app)

# --- Routers Modularizados (Versionados) ---
# Comente/descomente conforme cada router estiver pronto para import
# app.include_router(media_router, prefix="/api/v1/media", tags=["Media"])
# app.include_router(scene_router, prefix="/api/v1/scene", tags=["Scene"])
# app.include_router(face_router, prefix="/api/v1/facial", tags=["Facial"])
# app.include_router(voice_router, prefix="/api/v1/voice", tags=["Voice"])
# ... (demais routers)

# --- Endpoints Básicos ---

@app.get("/health", tags=["Utils"])
async def health_check():
    """
    Endpoint simples para verificar se a API está rodando.
    """
    return {"status": "ok", "message": "VisioVox API online"}

# --- Custom Exception Handler (Exemplo) ---

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler global para exceções não tratadas.
    """
    # TODO: Adicionar integração com i18n e logging
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            # "detail": t("errors.internal_server_error", language=lang)
        },
    )

# --- Eventos de Startup/Shutdown ---

@app.on_event("startup")
async def on_startup():
    """
    Evento de inicialização da API.
    - Inicializar conexões com Redis/Celery/etc.
    - Carregar configs globais, cache de traduções, etc.
    """
    # TODO: Inicializar integração com core, Celery, cache, etc.
    pass

@app.on_event("shutdown")
async def on_shutdown():
    """
    Evento de shutdown/graceful stop.
    - Fechar conexões, salvar logs, limpar recursos.
    """
    # TODO: Fechar conexões/limpar recursos.
    pass

# --- (Opcional) Customização OpenAPI Docs com exemplos multilíngues ---
# TODO: Adicionar customização de OpenAPI se necessário

# --- Ponto de Entrada (para uvicorn) ---
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("visiovox.apis.main:app", host="0.0.0.0", port=8000, reload=True)
