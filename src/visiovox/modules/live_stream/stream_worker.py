from abc import ABC, abstractmethod
from typing import Any, Union, Dict

from visiovox.core.config_manager import ConfigManager

class BaseStreamWorker(ABC):
    """
    Interface base para workers de streaming ao vivo.
    Define o contrato para execução e parada do loop de captura/processamento/transmissão.
    """

    @abstractmethod
    def run(self) -> None:
        """
        Executa o loop principal de captura, processamento e transmissão do stream.
        """
        pass

    @abstractmethod
    def stop(self) -> None:
        """
        Para o worker e libera todos os recursos.
        """
        pass

class OpenCVStreamWorker(BaseStreamWorker):
    """
    Worker de streaming ao vivo utilizando OpenCV para captura e transmissão.
    Permite integração com pipelines de processamento multimodal.
    """

    def __init__(self, input_source: Union[str, int], output_target: str, pipeline: Any, config: Union[ConfigManager, Dict]) -> None:
        """
        Inicializa o worker de streaming com OpenCV.

        Args:
            input_source (str | int): Fonte de entrada (webcam index, path, RTMP URL, etc).
            output_target (str): Destino do stream processado (arquivo, RTMP, display).
            pipeline (Any): Pipeline de processamento a ser aplicado ao stream.
            config (ConfigManager | dict): Configuração global ou específica.
        """
        self.input_source = input_source
        self.output_target = output_target
        self.pipeline = pipeline
        self.config = config
        self._running = False
        # TODO: Inicializar recursos do OpenCV

    def run(self) -> None:
        """
        Executa o loop principal de captura, processamento e transmissão usando OpenCV.
        """
        # TODO: Implementar loop de captura/processamento/transmissão
        pass

    def stop(self) -> None:
        """
        Para o worker e libera recursos do OpenCV.
        """
        # TODO: Implementar liberação de recursos
        pass 