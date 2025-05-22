from abc import ABC, abstractmethod
from typing import Any, Union
from pathlib import Path

from visiovox.core.config_manager import ConfigManager

class BaseFaceSwapper(ABC):
    """
    Interface abstrata para módulos de face swap.

    Métodos:
        swap: Realiza a troca de faces usando modelo especificado.
    """
    @abstractmethod
    def swap(self, source_face: Any, target_frame: Any, model_name: str) -> Any:
        """
        Realiza a troca de faces entre a imagem fonte e o quadro alvo.

        Args:
            source_face (Any): Imagem ou embedding da face de origem.
            target_frame (Any): Frame ou imagem alvo para aplicar a troca.
            model_name (str): Nome do modelo de face swap a ser utilizado.

        Returns:
            Any: Frame ou imagem processada com a face trocada.
        """
        pass

class InSwapperFaceSwapper(BaseFaceSwapper):
    """
    Implementação concreta de face swap usando InSwapper (InsightFace).

    Args:
        model_path (str | Path): Caminho para o modelo ONNX ou equivalente.
        config (ConfigManager | dict): Configurações gerais ou específicas do modelo.
    """
    def __init__(self, model_path: Union[str, Path], config: Union[ConfigManager, dict]) -> None:
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Inicializar modelo ONNX/InSwapper

    def swap(self, source_face: Any, target_frame: Any, model_name: str) -> Any:
        # TODO: Implementar chamada ao modelo de swap
        pass 