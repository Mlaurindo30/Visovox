import pytest
from fastapi.testclient import TestClient
from concurrent.futures import ThreadPoolExecutor
from src.visiovox.apis.main import app

client = TestClient(app)

def upload_sample():
    with open("tests/assets/sample.jpg", "rb") as img:
        response = client.post(
            "/scene_analysis/analyze",
            files={"file": ("sample.jpg", img, "image/jpeg")},
            data={"media_type": "image", "params": '{"detect_mode": "YOLOFace"}'}
        )
    return response

def test_concurrent_uploads():
    n = 10  # Simule 10 uploads concorrentes
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(upload_sample) for _ in range(n)]
        results = [f.result() for f in futures]
    for r in results:
        assert r.status_code == 200
        assert "task_id" in r.json()

def test_payload_edge_cases():
    # Payload sem file nem URL
    r = client.post("/scene_analysis/analyze", data={"media_type": "image"})
    assert r.status_code == 400
    # Params inválido
    r = client.post(
        "/scene_analysis/analyze",
        data={"media_type": "image", "params": '{"detect_mode": [1,2,3]'}
    )
    assert r.status_code in (400, 422)
