"""
Pacote live_stream do VisioVox Fusion.
Orquestra streaming ao vivo de vídeo/áudio e gerenciamento de workers para pipelines em tempo real.
"""

from .stream_orchestrator import BaseLiveStreamOrchestrator, DefaultLiveStreamOrchestrator
from .stream_worker import BaseStreamWorker, OpenCVStreamWorker

__all__ = [
    "BaseLiveStreamOrchestrator",
    "DefaultLiveStreamOrchestrator",
    "BaseStreamWorker",
    "OpenCVStreamWorker",
]

# --- Notas e Recomendações ---
# O uso de ABCs (Abstract Base Classes) garante plugabilidade futura (ex: implementação de GStreamerWorker, WebRTCWorker etc.).
# O padrão permite expansão para múltiplos protocolos/backends sem alterar interfaces públicas.
# Métodos aceitam input_source flexível (str, int, RTMP, etc), essencial para pipelines multimodais em diferentes ambientes.
# Estrutura pronta para paralelismo, threads ou processamento assíncrono, a depender da estratégia de implementação futura (threading, multiprocessing, asyncio).
# Extensibilidade: Basta criar novos workers/orchestrators herdando das bases e registrar hooks/callbacks para monitoramento.
# Integração: O orquestrador está pronto para ser consumido pelo PipelineManager/Core e integrado via API (ex: endpoints de "iniciar/encerrar live" na API FastAPI).
# Preparado para testes unitários: workers podem ser mockados e hooks testados independentemente. 