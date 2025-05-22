from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, Union

from visiovox.core.config_manager import ConfigManager

class BaseLiveStreamOrchestrator(ABC):
    """
    Interface base para orquestradores de streaming ao vivo.
    Define o contrato para iniciar e parar o stream.
    """

    @abstractmethod
    def start_stream(self, input_source: Union[str, int], output_target: str, pipeline: Any, params: Optional[Dict] = None) -> None:
        """
        Inicia o streaming ao vivo, conectando input ao pipeline de processamento e output.

        Args:
            input_source (str | int): Fonte de entrada (webcam index, path, RTMP URL, etc).
            output_target (str): Destino do stream processado (arquivo, RTMP, display).
            pipeline (Any): Pipeline de processamento a ser aplicado ao stream.
            params (dict, opcional): Parâmetros extras de configuração.
        """
        pass

    @abstractmethod
    def stop_stream(self) -> None:
        """
        Encerra o streaming ao vivo, liberando todos os recursos.
        """
        pass

class DefaultLiveStreamOrchestrator(BaseLiveStreamOrchestrator):
    """
    Implementação padrão do orquestrador de streaming ao vivo.
    Gerencia captura, processamento e transmissão em tempo real.
    """

    def __init__(self, config: Union[ConfigManager, Dict]) -> None:
        """
        Inicializa o orquestrador de streaming ao vivo.

        Args:
            config (ConfigManager | dict): Configuração global ou específica.
        """
        self.config = config
        self._is_streaming = False
        self._worker = None  # Worker de stream em execução

    def start_stream(self, input_source: Union[str, int], output_target: str, pipeline: Any, params: Optional[Dict] = None) -> None:
        """
        Inicia o streaming ao vivo.

        Args:
            input_source (str | int): Fonte de entrada.
            output_target (str): Destino do stream.
            pipeline (Any): Pipeline de processamento.
            params (dict, opcional): Parâmetros extras.
        """
        # TODO: Instanciar e iniciar worker de stream.
        pass

    def stop_stream(self) -> None:
        """
        Encerra o streaming e libera recursos.
        """
        # TODO: Encerrar worker e liberar recursos.
        pass 