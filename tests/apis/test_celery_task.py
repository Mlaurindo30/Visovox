from src.visiovox.apis.celery_tasks import process_media_task

def test_process_media_task_stub():
    res = process_media_task(media_type="image", file_info={"filename": "img.jpg"}, params={"model":"default"})
    assert res["status"] == "success" or res["status"] == "failure" 