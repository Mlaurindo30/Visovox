from fastapi import APIRouter, UploadFile, File, Form, Request, HTTPException, BackgroundTasks, status, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from src.visiovox.apis.schemas import (
    SceneAnalysisRequest, SceneAnalysisResponse, TaskStatusResponse, ErrorResponse
)
from src.visiovox.apis.celery_tasks import process_scene_task
from src.visiovox.apis.i18n import t
import uuid
import logging

router = APIRouter(prefix="/scene_analysis", tags=["Scene Analysis"])
logger = logging.getLogger("scene_analysis")

@router.post(
    "/analyze",
    response_model=SceneAnalysisResponse,
    responses={400: {"model": ErrorResponse}},
    summary="Analisa uma cena (imagem ou vídeo) para detecção facial, landmarks, segmentação etc.",
)
async def analyze_scene(
    request: Request,
    media_type: str = Form(..., description="Tipo de mídia ('image' ou 'video')"),
    file: Optional[UploadFile] = File(None, description="Arquivo de mídia"),
    media_url: Optional[str] = Form(None, description="URL remota da mídia (opcional)"),
    params: Optional[str] = Form(None, description="Parâmetros extras em JSON (opcional)"),
):
    import json
    if not file and not media_url:
        raise HTTPException(status_code=400, detail=t("file_or_url_required"))
    try:
        params_dict = json.loads(params) if params else {}
    except Exception as e:
        logger.warning(f"Params inválidos: {params}")
        params_dict = {}
    task_id = str(uuid.uuid4())
    result = process_scene_task.delay(
        media_type,
        file.filename if file else None,
        media_url,
        params_dict,
        task_id=task_id
    )
    logger.info(f"Tarefa Celery enviada: {result.id}")
    return SceneAnalysisResponse(
        task_id=result.id,
        status="queued",
        result=None,
        message=t("scene_analysis_queued"),
        detail=None
    )

@router.get(
    "/status/{task_id}",
    response_model=TaskStatusResponse,
    responses={404: {"model": ErrorResponse}},
    summary="Consulta o status/resultados de uma análise de cena.",
)
async def get_task_status(task_id: str):
    from celery.result import AsyncResult
    task = AsyncResult(task_id)
    if not task:
        raise HTTPException(status_code=404, detail=t("task_not_found"))
    status = task.status.lower()
    result = task.result if task.successful() else None
    return TaskStatusResponse(
        task_id=task_id,
        status=status,
        progress=task.info.get("progress") if task.info else None,
        message=task.info.get("message") if task.info else None,
        result=result
    )

# (Opcional) Endpoints adicionais:
# @router.get("/result/{id}", ...)
# @router.get("/list", ...)

return router 