import pytest
from fastapi.testclient import TestClient
import celery.app.task

def mock_celery(monkeypatch):
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_media_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_media_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.routers.media_ingestion_router.process_media_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.routers.media_ingestion_router.process_media_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_facial_processing_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_facial_processing_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_voice_processing_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_voice_processing_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.generate_visual_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.generate_visual_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_scene_analysis_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_scene_analysis_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_multimodal_sync_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.process_multimodal_sync_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.start_live_stream_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.start_live_stream_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.download_model_task.delay", lambda *args, **kwargs: type("T", (), {"id": "12345"})())
    monkeypatch.setattr("src.visiovox.apis.celery_tasks.download_model_task.apply_async", lambda *args, **kwargs: type("T", (), {"id": "12345"})())

@pytest.fixture
def client(monkeypatch):
    mock_celery(monkeypatch)
    from src.visiovox.apis.main import app
    return TestClient(app)

def test_process_media_missing_file(client):
    response = client.post("/api/v1/media/process", data={"media_type": "image"})
    assert response.status_code == 400

def test_process_media_ok(monkeypatch):
    monkeypatch.setattr(celery.app.task.Task, "apply_async", lambda self, *args, **kwargs: type("T", (), {"id": "12345"})())
    from src.visiovox.apis.main import app
    from fastapi.testclient import TestClient
    client = TestClient(app)
    with open("tests/assets/sample.jpg", "rb") as f:
        response = client.post(
            "/api/v1/media/process",
            data={"media_type": "image"},
            files={"file": ("sample.jpg", f, "image/jpeg")}
        )
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_status_multilanguage(client, monkeypatch):
    class DummyResult:
        state = "SUCCESS"
        info = {"result": {"output_path": "/tmp/output/image_result.mp4"}}
    monkeypatch.setattr("src.visiovox.apis.routers.media_ingestion_router.AsyncResult", lambda tid: DummyResult())
    response = client.get("/api/v1/media/status/12345", headers={"accept-language": "pt"})
    assert response.status_code == 200
    assert "result" in response.json()

def test_facial_processing(client):
    response = client.post("/api/v1/face/process", json={"media_type": "image", "media_url": "http://teste/img.jpg", "params": {}})
    assert response.status_code in (200, 202, 400)

def test_voice_processing(client):
    response = client.post("/api/v1/voice/process", json={"media_type": "audio", "media_url": "http://teste/audio.wav", "params": {}})
    assert response.status_code in (200, 202, 400)

def test_visual_generation(client):
    response = client.post("/api/v1/visual/generate", json={"media_type": "image", "media_url": "http://teste/img.jpg", "params": {}})
    assert response.status_code in (200, 202, 400)

def test_scene_analysis(client):
    response = client.post("/api/v1/scene/analyze", json={"media_type": "image", "media_url": "http://teste/img.jpg", "params": {}})
    assert response.status_code in (200, 202, 400)

def test_multimodal_sync(client):
    response = client.post("/api/v1/sync/process", json={"media_type": "video", "media_url": "http://teste/video.mp4", "params": {}})
    assert response.status_code in (200, 202, 400)

def test_live_stream_start(client):
    response = client.post("/api/v1/live/start", json={"media_type": "video", "media_url": "http://teste/stream", "params": {}})
    assert response.status_code in (200, 202, 400)

def test_model_management_download(client):
    response = client.post("/api/v1/models/download", json={"media_type": "model", "media_url": "http://teste/model", "params": {}})
    assert response.status_code in (200, 202, 400) 