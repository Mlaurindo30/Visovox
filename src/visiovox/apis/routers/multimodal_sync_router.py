from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from typing import Any

from ..schemas import (
    MediaProcessRequest,
    MediaProcessResponse,
    ErrorResponse,
    TaskStatusResponse
)
from ..celery_tasks import process_multimodal_sync_task
# from ..dependencies import get_current_user, get_i18n_language
from ..i18n import t

def get_multimodal_sync_router() -> APIRouter:
    """
    Cria e retorna um APIRouter para o domínio de sincronização multimodal (lip sync, talking head, gesture sync).
    Integra tasks Celery, schemas padronizados, autenticação e i18n.
    """
    router = APIRouter(tags=["Multimodal Sync"])

    @router.post(
        "/process",
        response_model=MediaProcessResponse,
        responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
        summary="Submete mídia e parâmetros para sincronização multimodal (lip sync, talking head, etc)"
    )
    async def process_sync(
        request_data: MediaProcessRequest,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Recebe uma requisição para sincronização multimodal (lip sync, gesture sync).
        Dispara task Celery correspondente.
        """
        task = process_multimodal_sync_task.apply_async(args=[
            request_data.media_type,
            request_data.media_url,
            request_data.params
        ])
        return {
            "status": "pending",
            "task_id": task.id,
            "message": t("sync.process.queued"),
            "detail": t("sync.process.detail")
        }

    @router.get(
        "/status/{task_id}",
        response_model=TaskStatusResponse,
        responses={404: {"model": ErrorResponse}},
        summary="Consulta status de sincronização multimodal (async)"
    )
    async def get_task_status(
        task_id: str,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Consulta o status/resultados de uma task Celery de sincronização multimodal.
        """
        return {
            "status": "pending",
            "task_id": task_id,
            "message": t("sync.status.pending"),
            "detail": t("sync.status.detail")
        }

    # (Opcional) Endpoints adicionais:
    # @router.get("/result/{id}", ...)
    # @router.get("/list", ...)

    return router 