from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Union

try:
    import numpy as np
    from PIL import Image
except ImportError:
    np = None
    Image = None

from ...core.config_manager import ConfigManager

class BaseVisualGenerator(ABC):
    """
    Interface base para geradores de imagens visuais.
    Todos os geradores (GAN, Diffusion, etc.) devem herdar desta classe.
    """

    @abstractmethod
    def generate(self, params: Dict[str, Any]) -> Any:
        """
        Gera uma imagem sintética condicionalmente aos parâmetros fornecidos.

        Args:
            params (dict): Parâmetros para condicionar a geração (vetor latente, atributos, etc).

        Returns:
            Any: Imagem gerada (np.ndarray, PIL.Image ou path).
        """
        pass

class StyleGANEXVisualGenerator(BaseVisualGenerator):
    """
    Gerador visual baseado em StyleGANEX, permite geração e manipulação condicional de faces/estilos.

    Args:
        model_path (str | Path): Caminho para o modelo StyleGANEX.
        config (ConfigManager | dict): Configuração do sistema ou do modelo.
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        config: Union[ConfigManager, Dict[str, Any]],
    ) -> None:
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Carregar modelo StyleGANEX

    def generate(self, params: Dict[str, Any]) -> Any:
        """
        Gera uma imagem usando StyleGANEX, condicionado pelos parâmetros.

        Args:
            params (dict): Parâmetros (vetor latente, atributos, seed, etc).

        Returns:
            Any: Imagem gerada (np.ndarray, PIL.Image ou caminho do arquivo).
        """
        # TODO: Implementar inferência com StyleGANEX
        pass 