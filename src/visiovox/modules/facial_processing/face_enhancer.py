from abc import ABC, abstractmethod
from typing import Any, Union
from pathlib import Path

from visiovox.core.config_manager import ConfigManager

class BaseFaceEnhancer(ABC):
    """
    Interface abstrata para aprimoramento de faces (face enhancement).
    """
    @abstractmethod
    def enhance(self, face_image: Any, model_name: str) -> Any:
        """
        Aprimora a qualidade de uma imagem facial usando modelo específico.

        Args:
            face_image (Any): Imagem da face para aprimoramento.
            model_name (str): Nome do modelo a ser utilizado.

        Returns:
            Any: Imagem aprimorada.
        """
        pass

class GFPGANFaceEnhancer(BaseFaceEnhancer):
    """
    Implementação concreta usando GFPGAN.
    """
    def __init__(self, model_path: Union[str, Path], config: Union[ConfigManager, dict]) -> None:
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Inicializar modelo GFPGAN

    def enhance(self, face_image: Any, model_name: str) -> Any:
        # TODO: Aplicar aprimoramento via GFPGAN
        pass 