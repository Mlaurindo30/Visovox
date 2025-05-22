from abc import ABC, abstractmethod
from typing import Any, Union

from ...core.config_manager import ConfigManager

class BasePitchProcessor(ABC):
    """
    Interface abstrata para processadores de pitch/timbre.
    Permite manipulação paramétrica de voz (ex: pitch shifting).
    """
    @abstractmethod
    def change_pitch(self, audio: Any, semitones: float) -> Any:
        """
        Altera o pitch do áudio.

        Args:
            audio (Any): Áudio de entrada.
            semitones (float): Valor de alteração em semitons (+/-).

        Returns:
            Any: Áudio com pitch alterado.
        """
        pass

class DefaultPitchProcessor(BasePitchProcessor):
    """
    Implementação padrão de alteração de pitch (ex: usando librosa/pydub).
    """
    def __init__(self, config: Union[ConfigManager, dict]) -> None:
        """
        Inicializa o processador de pitch com configurações.

        Args:
            config (ConfigManager | dict): Configuração global ou específica de pitch.
        """
        self.config = config
        # TODO: Inicializar backend de manipulação de pitch

    def change_pitch(self, audio: Any, semitones: float) -> Any:
        """
        Altera o pitch do áudio pelo valor especificado em semitons.

        Args:
            audio (Any): Áudio de entrada.
            semitones (float): Valor de alteração do pitch.

        Returns:
            Any: Áudio processado.
        """
        # TODO: Implementar lógica de pitch shifting
        pass 