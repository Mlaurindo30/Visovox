# Módulo Core — VisioVox Fusion

## Visão Geral
- PipelineManager centraliza registro e execução de pipelines.
- Suporte a plug & play de detectores, extractores, segmentadores.
- Logging estruturado e pronto para observabilidade.

## Exemplo de Uso
```python
from src.visiovox.core.pipeline_manager import PipelineManager
pm = PipelineManager()
result = pm.run_pipeline("scene_analysis", input_data)
```

## Dicas de Expansão
- Para plugar novo detector, importe e instancie no run_pipeline.
- Use campos opcionais nos resultados para evolução incremental.
- Logging detalhado para cada execução de pipeline.

## Observabilidade
- Pronto para integração com Sentry e Prometheus.
- Healthcheck pode consultar status dos pipelines/modelos.

---

**Core pronto para evolução incremental, integração plugável e automação!** 