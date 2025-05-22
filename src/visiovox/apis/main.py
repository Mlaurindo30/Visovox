from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.media_ingestion_router import get_media_ingestion_router
from .routers.scene_analysis_router import get_scene_analysis_router
from .routers.facial_processing_router import get_facial_processing_router
from .routers.voice_processing_router import get_voice_processing_router
from .routers.multimodal_sync_router import get_multimodal_sync_router
from .routers.visual_generation_router import get_visual_generation_router
from .routers.live_stream_router import get_live_stream_router
from .routers.model_management_router import get_model_management_router
# Importe outros routers conforme criados

from .middlewares import (
    add_logging_middleware,
    add_rate_limit_middleware,
    add_i18n_middleware,
    add_error_handling_middleware,
)

app = FastAPI(title="VisioVox Fusion API", version="1.0.0")

# Middlewares globais
add_logging_middleware(app)
add_rate_limit_middleware(app)
add_i18n_middleware(app)
add_error_handling_middleware(app)

# CORS (ajuste allow_origins para produção)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers versionados
app.include_router(get_media_ingestion_router(), prefix="/api/v1/media")
app.include_router(get_scene_analysis_router(), prefix="/api/v1/scene")
app.include_router(get_facial_processing_router(), prefix="/api/v1/face")
app.include_router(get_voice_processing_router(), prefix="/api/v1/voice")
app.include_router(get_multimodal_sync_router(), prefix="/api/v1/sync")
app.include_router(get_visual_generation_router(), prefix="/api/v1/visual")
app.include_router(get_live_stream_router(), prefix="/api/v1/live")
app.include_router(get_model_management_router(), prefix="/api/v1/models")
# Siga o mesmo padrão para novos domínios

# Pronto para documentação interativa, testes e expansão incremental 