import pytest
from fastapi.testclient import TestClient
from src.visiovox.apis.main import app
from src.visiovox.apis.schemas import SceneAnalysisRequest, SceneAnalysisResponse

@pytest.fixture
def client():
    return TestClient(app)

def mock_celery(monkeypatch):
    import celery.app.task
    monkeypatch.setattr(celery.app.task.Task, "apply_async", lambda self, *args, **kwargs: type("T", (), {"id": "abc123"})())

# Teste: Detecção facial básica
def test_scene_analysis_basic(client, monkeypatch):
    mock_celery(monkeypatch)
    payload = {
        "media_type": "image",
        "params": {"detect_mode": "YOLOFace", "max_faces": 1}
    }
    response = client.post("/api/v1/scene/analyze", json=payload)
    assert response.status_code in (200, 202)
    data = response.json()
    assert "task_id" in data
    assert data["status"] in ("success", "queued", "started")
    assert "result" in data
    assert data["result"]["num_faces"] >= 0
    assert "faces" in data["result"]

# Teste: Resposta com landmarks e máscara
def test_scene_analysis_landmarks_mask(client, monkeypatch):
    mock_celery(monkeypatch)
    payload = {
        "media_type": "image",
        "params": {"detect_mode": "YOLOFace", "landmark_mode": "68", "segment": True, "max_faces": 1}
    }
    response = client.post("/api/v1/scene/analyze", json=payload)
    assert response.status_code in (200, 202)
    data = response.json()
    assert "task_id" in data
    assert "result" in data
    face = data["result"]["faces"][0]
    assert "landmarks" in face or "masks" in face
    if "landmarks" in face:
        assert isinstance(face["landmarks"], list)
    if "masks" in face:
        assert isinstance(face["masks"], list)

# Teste: Resposta para vídeo (frame a frame)
def test_scene_analysis_video_frame(client, monkeypatch):
    mock_celery(monkeypatch)
    payload = {
        "media_type": "video",
        "params": {"detect_mode": "YOLOFace", "max_faces": 2, "frame_id": 5}
    }
    response = client.post("/api/v1/scene/analyze", json=payload)
    assert response.status_code in (200, 202)
    data = response.json()
    assert "task_id" in data
    assert "result" in data
    assert "frame_id" in data["result"]
    assert "faces" in data["result"]

# Teste: media_type inválido
def test_scene_analysis_invalid_media_type(client, monkeypatch):
    mock_celery(monkeypatch)
    payload = {"media_type": "audio", "params": {}}
    response = client.post("/api/v1/scene/analyze", json=payload)
    assert response.status_code in (400, 422)
    data = response.json()
    assert "error" in data or "detail" in data

# Teste: ausência de params obrigatórios
def test_scene_analysis_missing_params(client, monkeypatch):
    mock_celery(monkeypatch)
    payload = {"media_type": "image"}
    response = client.post("/api/v1/scene/analyze", json=payload)
    assert response.status_code in (200, 202, 400, 422)
    data = response.json()
    assert "task_id" in data or "error" in data or "detail" in data

# Teste: payload vazio
def test_scene_analysis_empty_payload(client, monkeypatch):
    mock_celery(monkeypatch)
    response = client.post("/api/v1/scene/analyze", json={})
    assert response.status_code in (400, 422)
    data = response.json()
    assert "error" in data or "detail" in data

# Teste: tentativa sem autenticação (se aplicável)
def test_scene_analysis_unauthenticated(monkeypatch):
    # Simula client sem autenticação, se o endpoint exigir token/JWT
    from fastapi.testclient import TestClient
    client = TestClient(app)
    mock_celery(monkeypatch)
    payload = {"media_type": "image", "params": {}}
    response = client.post("/api/v1/scene/analyze", json=payload)
    # Se exigir autenticação, espera 401. Se não, espera 200/202/400/422
    assert response.status_code in (200, 202, 400, 401, 422) 