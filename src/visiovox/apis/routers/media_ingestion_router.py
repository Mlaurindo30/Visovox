from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional
from src.visiovox.apis.schemas import (
    MediaProcessRequest,
    MediaProcessResponse,
    TaskStatusResponse,
    ErrorResponse,
)
from src.visiovox.apis.celery_tasks import process_media_task
from src.visiovox.core.logger_setup import setup_logging
# from src.visiovox.apis.dependencies import get_current_user  # Descomente se autenticação for obrigatória
from src.visiovox.utils.i18n import t  # Supondo helper t() já implementado

from celery.result import AsyncResult
import logging
import json

def get_media_ingestion_router() -> APIRouter:
    """
    Router para ingestão e processamento de mídia (imagem, vídeo, áudio).
    Permite upload, ingestão remota, dispara processamento assíncrono via Celery e consulta status.
    """
    router = APIRouter(tags=["media_ingestion"])
    logger = logging.getLogger("media_ingestion")

    @router.post(
        "/process",
        response_model=MediaProcessResponse,
        responses={400: {"model": ErrorResponse}},
        summary="Processar mídia (imagem, vídeo, áudio) via pipeline assíncrono",
    )
    async def process_media_endpoint(
        request: Request,
        media_type: str = Form(..., description="Tipo de mídia: image, video, audio"),
        file: Optional[UploadFile] = File(None, description="Arquivo de mídia"),
        media_url: Optional[str] = Form(None, description="URL remota para baixar a mídia"),
        params: Optional[str] = Form(None, description="Parâmetros extras do pipeline (JSON serializado)"),
        # user: dict = Depends(get_current_user),  # Descomente se for endpoint protegido
    ):
        """
        Recebe mídia (upload ou URL), valida e dispara processamento assíncrono via Celery.
        Retorna task_id e status inicial.
        """
        lang = request.headers.get("accept-language", "en")
        logger.info(f"Recebendo pedido de processamento de mídia | media_type={media_type} | user_agent={request.headers.get('user-agent')}")

        # Validação mínima (camada extra ao schema)
        if not file and not media_url:
            msg = t("Você deve fornecer um arquivo de mídia ou uma URL.", lang)
            logger.warning(f"Requisição inválida: sem arquivo nem URL")
            raise HTTPException(status_code=400, detail=msg)

        # Decodifica params se vier como JSON string
        params_dict = {}
        if params:
            try:
                params_dict = json.loads(params)
            except Exception:
                logger.warning(f"Parâmetros extras inválidos: {params}")
                msg = t("Parâmetros extras devem ser um JSON válido.", lang)
                raise HTTPException(status_code=400, detail=msg)

        # Aqui você poderia salvar o arquivo para disco/temp e passar caminho à Celery Task
        # Para simplificação, passaremos info mínima (adapte para path real no futuro)
        file_info = {"filename": file.filename} if file else None

        celery_args = {
            "media_type": media_type,
            "file_info": file_info,
            "media_url": media_url,
            "params": params_dict,
            # "user_id": user["id"]  # se autenticação implementada
        }
        logger.info(f"Disparando task Celery com args: {celery_args}")

        celery_task = process_media_task.delay(**celery_args)

        return MediaProcessResponse(
            task_id=celery_task.id,
            status="queued",
            message=t("Mídia enviada com sucesso. Processamento iniciado!", lang),
        )

    @router.get(
        "/status/{task_id}",
        response_model=TaskStatusResponse,
        responses={404: {"model": ErrorResponse}},
        summary="Consulta status de processamento de mídia (Celery task)",
    )
    async def get_task_status_endpoint(
        request: Request,
        task_id: str,
        # user: dict = Depends(get_current_user),  # Descomente se proteção necessária
    ):
        """
        Consulta status/resultados reais da task Celery.
        """
        lang = request.headers.get("accept-language", "en")
        celery_result = AsyncResult(task_id)
        logger.info(f"Consulta de status para task_id={task_id}: state={celery_result.state}")

        if celery_result.state == "PENDING":
            return TaskStatusResponse(
                task_id=task_id,
                status="queued",
                message=t("Processamento aguardando na fila.", lang),
            )
        elif celery_result.state == "STARTED":
            meta = celery_result.info or {}
            return TaskStatusResponse(
                task_id=task_id,
                status="started",
                progress=meta.get("progress"),
                message=t("Processando...", lang),
            )
        elif celery_result.state == "SUCCESS":
            meta = celery_result.info or {}
            return TaskStatusResponse(
                task_id=task_id,
                status="success",
                result=meta.get("result"),
                message=t("Processamento concluído com sucesso.", lang),
            )
        elif celery_result.state == "FAILURE":
            error = str(celery_result.info)
            logger.error(f"Task {task_id} falhou: {error}")
            return JSONResponse(
                status_code=500,
                content=ErrorResponse(
                    error="Processamento falhou",
                    message=error,
                    code=500
                ).dict()
            )
        else:
            return TaskStatusResponse(
                task_id=task_id,
                status=celery_result.state.lower(),
                message=t(f"Status atual: {celery_result.state}", lang)
            )

    return router 