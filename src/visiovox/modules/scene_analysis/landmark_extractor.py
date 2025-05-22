from abc import ABC, abstractmethod
from typing import Any, List, Union
from pathlib import Path
from visiovox.core.config_manager import ConfigManager

class BaseLandmarkExtractor(ABC):
    """
    Interface base para extração de landmarks faciais.
    """

    @abstractmethod
    def extract(self, image: Any) -> List[List[float]]:
        """
        Extrai pontos faciais (landmarks) de uma imagem.

        Args:
            image (Any): Imagem de entrada.

        Returns:
            List[List[float]]: Lista de listas de coordenadas dos landmarks.
        """
        pass

class FanLandmarkExtractor(BaseLandmarkExtractor):
    """
    Extrator de landmarks usando FAN (Face Alignment Network).
    """

    def __init__(self, model_path: Union[str, Path], config: Union[ConfigManager, dict]) -> None:
        """
        Inicializa o extrator FAN.

        Args:
            model_path (str | Path): Caminho do modelo FAN.
            config (ConfigManager | dict): Configuração.
        """
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Carregar modelo FAN

    def extract(self, image: Any) -> List[List[float]]:
        """
        Extrai landmarks faciais da imagem.

        Args:
            image (Any): Imagem.

        Returns:
            List[List[float]]: Lista de coordenadas de landmarks.
        """
        # TODO: Implementar extração real usando FAN
        pass 