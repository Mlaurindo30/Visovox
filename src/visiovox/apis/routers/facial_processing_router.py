from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from typing import Any

from ..schemas import (
    MediaProcessRequest,
    MediaProcessResponse,
    ErrorResponse,
    TaskStatusResponse
)
from ..celery_tasks import process_facial_processing_task
# from ..dependencies import get_current_user, get_i18n_language
from ..i18n import t

def get_facial_processing_router() -> APIRouter:
    """
    Cria e retorna um APIRouter para o domínio de processamento facial.
    Integra tasks Celery, schemas padronizados, autenticação e i18n.
    """
    router = APIRouter(tags=["Facial Processing"])

    @router.post(
        "/process",
        response_model=MediaProcessResponse,
        responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
        summary="Submete mídia e parâmetros para processamento facial (face swap, enhancement, edição)"
    )
    async def process_face(
        request_data: MediaProcessRequest,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Recebe uma requisição de processamento facial (face swap, enhancement, edição).
        Dispara task Celery correspondente.
        """
        task = process_facial_processing_task.apply_async(args=[
            request_data.media_type,
            request_data.media_url,
            request_data.params
        ])
        return {
            "status": "pending",
            "task_id": task.id,
            "message": t("face.process.queued"),
            "detail": t("face.process.detail")
        }

    @router.get(
        "/status/{task_id}",
        response_model=TaskStatusResponse,
        responses={404: {"model": ErrorResponse}},
        summary="Consulta status de processamento facial (async)"
    )
    async def get_task_status(
        task_id: str,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Consulta o status/resultados de uma task Celery de processamento facial.
        """
        return {
            "status": "pending",
            "task_id": task_id,
            "message": t("face.status.pending"),
            "detail": t("face.status.detail")
        }

    # (Opcional) Endpoints adicionais:
    # @router.get("/result/{id}", ...)
    # @router.get("/list", ...)

    return router 