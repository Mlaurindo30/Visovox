from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union
from pathlib import Path
from visiovox.core.config_manager import ConfigManager

class BaseFaceDetector(ABC):
    """
    Interface base para detectores faciais.
    """

    @abstractmethod
    def detect(self, image: Any) -> List[Dict[str, Any]]:
        """
        Detecta faces em uma imagem.

        Args:
            image (Any): Objeto imagem (ex: numpy array, PIL Image).

        Returns:
            List[Dict[str, Any]]: Lista de dicts com dados das faces detectadas
            (ex: {'box': [x1, y1, x2, y2], 'score': float}).
        """
        pass

class YOLOFaceDetector(BaseFaceDetector):
    """
    Detector facial baseado em modelo YOLO.
    """

    def __init__(self, model_path: Union[str, Path], config: Union[ConfigManager, dict]) -> None:
        """
        Inicializa o detector YOLO com o caminho do modelo e configurações.

        Args:
            model_path (str | Path): Caminho para o modelo YOLO.
            config (ConfigManager | dict): Configuração global ou específica.
        """
        self.model_path = Path(model_path)
        self.config = config
        # TODO: Carregar modelo YOLO aqui

    def detect(self, image: Any) -> List[Dict[str, Any]]:
        """
        Detecta faces usando o modelo YOLO.

        Args:
            image (Any): Imagem de entrada.

        Returns:
            List[Dict[str, Any]]: Lista de detecções de faces.
        """
        # TODO: Implementar detecção real com YOLO
        pass 