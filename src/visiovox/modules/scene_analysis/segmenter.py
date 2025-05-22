from abc import ABC, abstractmethod
from typing import Any, Union
from pathlib import Path
from visiovox.core.config_manager import ConfigManager

class BaseSegmenter(ABC):
    """
    Interface base para segmentação facial ou por regiões.
    """

    @abstractmethod
    def segment(self, image: Any) -> Any:
        """
        Segmenta regiões da face em uma imagem.

        Args:
            image (Any): Imagem de entrada.

        Returns:
            Any: Máscara, mapa de segmentos ou estrutura equivalente.
        """
        pass

class SAM2Segmenter(BaseSegmenter):
    """
    Segmentador baseado no modelo SAM2.
    """

    def __init__(self, model_path: Union[str, Path], config: Union[ConfigManager, dict]) -> None:
        """
        Inicializa o segmentador SAM2.

        Args:
            model_path (str | Path): Caminho para o modelo SAM2.
            config (ConfigManager | dict): Configuração.
        """
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Carregar modelo SAM2

    def segment(self, image: Any) -> Any:
        """
        Segmenta a imagem usando SAM2.

        Args:
            image (Any): Imagem.

        Returns:
            Any: Máscara segmentada ou estrutura de saída SAM2.
        """
        # TODO: Implementar segmentação real com SAM2
        pass 