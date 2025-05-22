from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    import numpy as np
    from PIL import Image
except ImportError:
    np = None
    Image = None

from ...core.config_manager import ConfigManager

class BaseDiffusionGenerator(ABC):
    """
    Interface base para geradores do tipo Diffusion (ex: StableDiffusion).
    """

    @abstractmethod
    def generate(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Gera uma imagem a partir de um prompt textual e parâmetros opcionais.

        Args:
            prompt (str): Descrição textual (prompt) para a geração.
            params (dict, opcional): Parâmetros adicionais (seed, steps, etc).

        Returns:
            Any: Imagem gerada (np.ndarray, PIL.Image ou caminho do arquivo).
        """
        pass

class StableDiffusionGenerator(BaseDiffusionGenerator):
    """
    Gerador visual baseado em modelos de Diffusion (ex: StableDiffusion).

    Args:
        model_path (str | Path): Caminho para o modelo Diffusion.
        config (ConfigManager | dict): Configuração do sistema ou do modelo.
    """

    def __init__(
        self,
        model_path: Union[str, Path],
        config: Union[ConfigManager, Dict[str, Any]],
    ) -> None:
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Carregar modelo Diffusion

    def generate(self, prompt: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """
        Gera uma imagem a partir de um prompt textual.

        Args:
            prompt (str): Prompt textual.
            params (dict, opcional): Parâmetros adicionais.

        Returns:
            Any: Imagem gerada (np.ndarray, PIL.Image ou caminho do arquivo).
        """
        # TODO: Implementar inferência com modelo Diffusion
        pass 