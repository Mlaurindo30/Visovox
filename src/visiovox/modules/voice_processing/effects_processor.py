from abc import ABC, abstractmethod
from typing import Any, Dict, Union

from ...core.config_manager import ConfigManager

class BaseVoiceEffectsProcessor(ABC):
    """
    Interface abstrata para aplicação de efeitos de áudio.
    Permite extensibilidade para múltiplos backends/bibliotecas.
    """
    @abstractmethod
    def apply_effects(self, audio: Any, effects: Dict) -> Any:
        """
        Aplica efeitos ao áudio.

        Args:
            audio (Any): Áudio de entrada (ex: numpy array, path, etc.).
            effects (dict): Dicionário com efeitos e parâmetros (ex: {"reverb": 0.2, "eq": [1,2,3]}).

        Returns:
            Any: Áudio processado com efeitos.
        """
        pass

class DefaultVoiceEffectsProcessor(BaseVoiceEffectsProcessor):
    """
    Implementação padrão de efeitos de áudio (ex: usando librosa, pydub).
    """
    def __init__(self, config: Union[ConfigManager, dict]) -> None:
        """
        Inicializa o processador de efeitos com configurações globais.

        Args:
            config (ConfigManager | dict): Configuração global ou específica de efeitos.
        """
        self.config = config
        # TODO: Inicializar libs de áudio/processamento conforme config

    def apply_effects(self, audio: Any, effects: Dict) -> Any:
        """
        Aplica efeitos ao áudio conforme parâmetros fornecidos.

        Args:
            audio (Any): Áudio de entrada.
            effects (dict): Parâmetros dos efeitos.

        Returns:
            Any: Áudio com efeitos aplicados.
        """
        # TODO: Implementar lógica de aplicação de efeitos usando backend escolhido
        pass 