from src.visiovox.core.pipeline_manager import PipelineManager

def test_pipeline_stub():
    manager = PipelineManager()
    res = manager.run_pipeline("media_ingestion", {"media_type":"image", "input_path":"path"})
    assert "output_path" in res and "meta" in res 