from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from typing import Any

from ..schemas import (
    MediaProcessRequest,
    MediaProcessResponse,
    TaskStatusResponse,
    ErrorResponse
)
from ..celery_tasks import start_live_stream_task, stop_live_stream_task
# from ..dependencies import get_current_user, get_i18n_language
from ..i18n import t

def get_live_stream_router() -> APIRouter:
    """
    Cria e retorna um APIRouter para o domínio de streaming ao vivo.
    Integra tasks Celery, schemas padronizados, autenticação e i18n.
    """
    router = APIRouter(tags=["Live Stream"])

    @router.post(
        "/start",
        response_model=MediaProcessResponse,
        responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
        summary="Inicia uma live stream com parâmetros de mídia"
    )
    async def start_live_stream(
        request_data: MediaProcessRequest,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Inicia uma sessão de live stream (webcam, RTMP, etc) e dispara task Celery se necessário.
        """
        task = start_live_stream_task.apply_async(args=[
            request_data.media_type,
            request_data.media_url,
            request_data.params
        ])
        return {
            "status": "pending",
            "task_id": task.id,
            "message": t("live.start.queued"),
            "detail": t("live.start.detail")
        }

    @router.post(
        "/stop",
        response_model=MediaProcessResponse,
        responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
        summary="Finaliza uma sessão de live stream"
    )
    async def stop_live_stream(
        session_id: str,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Finaliza uma sessão de live stream/processamento ao vivo.
        """
        task = stop_live_stream_task.apply_async(args=[
            session_id,
            None
        ])
        return {
            "status": "pending",
            "task_id": task.id,
            "message": t("live.stop.queued"),
            "detail": t("live.stop.detail")
        }

    @router.get(
        "/status/{session_id}",
        response_model=TaskStatusResponse,
        responses={404: {"model": ErrorResponse}},
        summary="Consulta status de uma sessão/processamento ao vivo"
    )
    async def get_live_stream_status(
        session_id: str,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Consulta o status/resultados de uma sessão de live stream.
        """
        return {
            "status": "pending",
            "session_id": session_id,
            "message": t("live.status.pending"),
            "detail": t("live.status.detail")
        }

    # (Opcional) Endpoint de snapshot/capture
    # @router.get("/snapshot/{session_id}", ...)

    return router 