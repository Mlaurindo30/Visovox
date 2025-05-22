from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from typing import Any

from ..schemas import (
    MediaProcessRequest,
    MediaProcessResponse,
    PaginatedResponse,
    ErrorResponse,
    TaskStatusResponse
)
from ..celery_tasks import download_model_task, update_model_task
# from ..dependencies import get_current_user, get_i18n_language
from ..i18n import t

def get_model_management_router() -> APIRouter:
    """
    Cria e retorna um APIRouter para o domínio de gerenciamento de modelos (download, atualização, remoção).
    Integra tasks Celery, schemas padronizados, autenticação e i18n.
    """
    router = APIRouter(tags=["Model Management"])

    @router.get(
        "/list",
        response_model=PaginatedResponse,
        responses={401: {"model": ErrorResponse}},
        summary="Lista todos os modelos disponíveis/baixados"
    )
    async def list_models(
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Lista modelos disponíveis e seus status/metadados.
        """
        # TODO: Consultar lista de modelos do manifesto/local, formatar resposta multilíngue
        pass

    @router.post(
        "/download",
        response_model=MediaProcessResponse,
        responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
        summary="Solicita download de um modelo específico"
    )
    async def download_model(
        request_data: MediaProcessRequest,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Solicita download (async) de um modelo indicado (por nome/id).
        """
        task = download_model_task.apply_async(args=[
            request_data.media_type,
            request_data.media_url,
            request_data.params
        ])
        return {
            "status": "pending",
            "task_id": task.id,
            "message": t("model.download.queued"),
            "detail": t("model.download.detail")
        }

    @router.get(
        "/status/{model_id}",
        response_model=TaskStatusResponse,
        responses={404: {"model": ErrorResponse}},
        summary="Consulta status de download/verificação de um modelo"
    )
    async def get_model_status(
        model_id: str,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Consulta status, progresso, hash, versão e erros de download/verificação de modelo.
        """
        return {
            "status": "pending",
            "task_id": model_id,
            "message": t("model.status.pending"),
            "detail": t("model.status.detail")
        }

    @router.delete(
        "/remove/{model_id}",
        response_model=MediaProcessResponse,
        responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}},
        summary="Remove modelo do cache local"
    )
    async def remove_model(
        model_id: str,
        request: Request,
        # current_user: Any = Depends(get_current_user),
    ) -> Any:
        """
        Remove modelo do cache local/disco.
        """
        # TODO: Remover modelo do storage/cache, checar permissões, multilíngue
        pass

    # (Opcional) Endpoint para atualizar/verificar todos modelos
    # @router.post("/update", ...)

    return router 