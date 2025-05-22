import pytest
from src.visiovox.apis.schemas import MediaProcessRequest, ErrorResponse, TaskStatusResponse, MediaProcessResponse

def test_media_process_request_valid():
    req = MediaProcessRequest(media_type="image", media_url="http://teste/img.jpg", params={"model":"default"})
    assert req.media_type == "image"

def test_media_process_request_invalid_type():
    with pytest.raises(ValueError):
        MediaProcessRequest(media_type=123, media_url="url")

def test_error_response_serialization():
    err = ErrorResponse(error="erro", message="msg", code=400)
    assert err.dict()["error"] == "erro"

def test_task_status_response():
    resp = TaskStatusResponse(task_id="abc", status="success", result={"output_path": "x"})
    assert resp.status == "success"

def test_media_process_response():
    resp = MediaProcessResponse(task_id="abc", status="queued", message="ok")
    assert resp.status == "queued" 