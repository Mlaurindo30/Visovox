"""
Módulo model_management do VisioVox Fusion.
Gerencia ciclo de vida, cache, download, validação e auditoria de modelos IA.
"""

from .model_manager import BaseModelManager, DefaultModelManager
from .model_manifest import ModelManifest
from .model_validator import ModelValidator
from .model_downloader import ModelDownloader
from .cache_manager import ModelCacheManager

__all__ = [
    "BaseModelManager",
    "DefaultModelManager",
    "ModelManifest",
    "ModelValidator",
    "ModelDownloader",
    "ModelCacheManager",
] 