"""
Módulo multimodal_sync da VisioVox Fusion.

Fornece interfaces e implementações para sincronização multimodal entre vídeo/frames e áudio,
incluindo lip sync (LatentSync) e gestos/expressão (futuro).
"""

from .lip_syncer import BaseLipSyncer, LatentSyncLipSyncer
from .gesture_syncer import BaseGestureSyncer, DefaultGestureSyncer

__all__ = [
    "BaseLipSyncer",
    "LatentSyncLipSyncer",
    "BaseGestureSyncer",
    "DefaultGestureSyncer",
] 