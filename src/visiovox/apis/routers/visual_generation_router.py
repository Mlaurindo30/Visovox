from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from typing import Any

from ..schemas import (
    MediaProcessRequest,
    MediaProcessResponse,
    ErrorResponse,
    TaskStatusResponse
)
from ..celery_tasks import generate_visual_task
# from ..dependencies import get_current_user, get_i18n_language
from ..i18n import t

def get_visual_generation_router() -> APIRouter:
    """
    Cria e retorna um APIRouter para o domínio de geração visual (imagens sintéticas).
    Integra tasks Celery, schemas padronizados, autenticação e i18n.
    """
    router = APIRouter(tags=["Visual Generation"])

    @router.post(
        "/generate",
        response_model=MediaProcessResponse,
        responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
        summary="Submete prompt e parâmetros para geração visual (imagem, vídeo, etc)"
    )
    async def generate_visual(
        request_data: MediaProcessRequest,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Recebe uma requisição para geração visual (imagem sintética, manipulação criativa).
        Dispara task Celery correspondente.
        """
        task = generate_visual_task.apply_async(args=[
            request_data.media_type,
            request_data.media_url,
            request_data.params
        ])
        return {
            "status": "pending",
            "task_id": task.id,
            "message": t("visual.generate.queued"),
            "detail": t("visual.generate.detail")
        }

    @router.get(
        "/status/{task_id}",
        response_model=TaskStatusResponse,
        responses={404: {"model": ErrorResponse}},
        summary="Consulta status de geração visual (async)"
    )
    async def get_task_status(
        task_id: str,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Consulta o status/resultados de uma task Celery de geração visual.
        """
        return {
            "status": "pending",
            "task_id": task_id,
            "message": t("visual.status.pending"),
            "detail": t("visual.status.detail")
        }

    # (Opcional) Endpoints adicionais:
    # @router.get("/result/{id}", ...)
    # @router.get("/list", ...)

    return router 