"""
Pacote core do VisioVox Fusion.

Fornece classes essenciais para orquestração de pipelines, gerenciamento de configuração,
logging estruturado e gerenciamento de recursos/modelos.
"""

from .config_manager import ConfigManager
from .logger_setup import setup_logging
from .resource_manager import ResourceManager
from .orchestrator import Orchestrator
from .pipeline_manager import PipelineManager

__all__ = [
    "ConfigManager",
    "setup_logging",
    "ResourceManager",
    "Orchestrator",
    "PipelineManager",
] 