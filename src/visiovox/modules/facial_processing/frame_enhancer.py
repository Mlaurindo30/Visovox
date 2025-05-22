from abc import ABC, abstractmethod
from typing import Any, Union
from pathlib import Path

from visiovox.core.config_manager import ConfigManager

class BaseFrameEnhancer(ABC):
    """
    Interface abstrata para aprimoramento de quadros completos (frame enhancement).
    """
    @abstractmethod
    def enhance(self, frame: Any, model_name: str) -> Any:
        """
        Aprimora a qualidade de um quadro de imagem ou vídeo.

        Args:
            frame (Any): Frame de imagem/vídeo.
            model_name (str): Nome do modelo a ser utilizado.

        Returns:
            Any: Frame aprimorado.
        """
        pass

class RealESRGANFrameEnhancer(BaseFrameEnhancer):
    """
    Implementação concreta usando RealESRGAN.
    """
    def __init__(self, model_path: Union[str, Path], config: Union[ConfigManager, dict]) -> None:
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Inicializar modelo RealESRGAN

    def enhance(self, frame: Any, model_name: str) -> Any:
        # TODO: Aplicar aprimoramento via RealESRGAN
        pass 