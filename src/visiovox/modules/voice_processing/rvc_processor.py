from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Dict, Union

from ...core.config_manager import ConfigManager

class BaseVoiceConverter(ABC):
    """
    Interface abstrata para conversores de voz.
    Garante padronização dos métodos de conversão para múltiplos backends/modelos.
    """
    @abstractmethod
    def convert(self, input_audio: Any, target_voice: str, params: Optional[Dict] = None) -> Any:
        """
        Converte o áudio de entrada para a voz/timbre alvo.

        Args:
            input_audio (Any): Áudio de entrada (ex: numpy array, path .wav, etc.).
            target_voice (str): Identificador/modelo da voz alvo.
            params (dict, opcional): Parâmetros adicionais para customização.

        Returns:
            Any: Áudio convertido (formato a definir na implementação).
        """
        pass

class RVCVoiceConverter(BaseVoiceConverter):
    """
    Implementação concreta de conversor de voz usando RVC (Retrieval-based Voice Conversion).
    """
    def __init__(self, model_path: Union[str, Path], config: Union[ConfigManager, dict]) -> None:
        """
        Inicializa o conversor RVC com o caminho do modelo e configuração.

        Args:
            model_path (str | Path): Caminho para o modelo RVC (.pth, .index, etc.).
            config (ConfigManager | dict): Configurações do sistema ou específicas do modelo.
        """
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Carregar modelo RVC e preparar pipeline

    def convert(self, input_audio: Any, target_voice: str, params: Optional[Dict] = None) -> Any:
        """
        Realiza a conversão de voz usando o modelo RVC carregado.

        Args:
            input_audio (Any): Áudio de entrada.
            target_voice (str): Voz/timbre alvo.
            params (dict, opcional): Parâmetros adicionais.

        Returns:
            Any: Áudio convertido.
        """
        # TODO: Implementar lógica de conversão de voz com RVC
        pass 