from fastapi import APIRouter
import redis
from celery.result import AsyncResult
import os

router = APIRouter(prefix="/healthz", tags=["Healthcheck"])

@router.get("/", summary="Healthcheck detalhado (API, Celery, Redis, Modelos)")
async def healthcheck():
    health = {"api": True}

    # Redis
    try:
        r = redis.Redis(host=os.getenv("REDIS_HOST", "localhost"), port=int(os.getenv("REDIS_PORT", 6379)))
        r.ping()
        health["redis"] = True
    except Exception as e:
        health["redis"] = False
        health["redis_error"] = str(e)

    # Celery
    try:
        from src.visiovox.apis.celery_tasks import celery_app
        insp = celery_app.control.inspect()
        active = insp.active()
        health["celery"] = bool(active)
    except Exception as e:
        health["celery"] = False
        health["celery_error"] = str(e)

    # Modelos
    try:
        from src.visiovox.core.model_management import ModelManager
        mm = ModelManager()
        status = mm.check_all_models()  # Implemente este método!
        health["models"] = status
    except Exception as e:
        health["models"] = False
        health["models_error"] = str(e)

    # GPU/CPU
    try:
        import torch
        health["cuda_available"] = torch.cuda.is_available()
    except Exception:
        health["cuda_available"] = False

    health["status"] = all([
        health.get("api"),
        health.get("redis"),
        health.get("celery"),
        health.get("models")
    ])
    return health 