from typing import Callable, List, Dict, Optional, Any
from src.visiovox.modules.scene_analysis.face_detector import YOLOFaceDetector
from src.visiovox.modules.scene_analysis.landmark_extractor import FanLandmarkExtractor
from src.visiovox.modules.scene_analysis.segmenter import SAM2Segmenter
import logging
import numpy as np

def load_image(path_or_url):
    # TODO: Implementar carregamento real de imagem (local ou remoto)
    # Aqui retorna um array dummy para simulação
    return np.zeros((256, 256, 3), dtype=np.uint8)

def save_overlay(image, faces):
    # TODO: Implementar geração e salvamento de overlay real
    return "/tmp/overlay_fake.png"

class PipelineManager:
    """
    Gerencia o registro e a recuperação de pipelines de processamento
    na VisioVox Fusion. Pipelines são sequências ordenadas de funções (steps)
    aplicadas em dados de entrada.
    """

    def __init__(self) -> None:
        """
        Inicializa o PipelineManager com um registro vazio de pipelines.
        """
        self._pipelines: Dict[str, List[Callable]] = {}

    def register_pipeline(self, name: str, steps: List[Callable]) -> None:
        """
        Registra um pipeline sob um nome específico.

        Args:
            name (str): Nome do pipeline.
            steps (list[callable]): Lista ordenada de funções/etapas do pipeline.
        """
        # TODO: Adicionar verificação de duplicidade ou sobrescrever com aviso
        self._pipelines[name] = steps

    def get_pipeline(self, name: str) -> Optional[List[Callable]]:
        """
        Retorna o pipeline registrado pelo nome.

        Args:
            name (str): Nome do pipeline.

        Returns:
            list[callable] | None: Lista de funções/etapas do pipeline, ou None se não encontrado.
        """
        return self._pipelines.get(name)

    def list_pipelines(self) -> List[str]:
        """
        Retorna uma lista com os nomes de todos os pipelines registrados.

        Returns:
            list[str]: Lista dos nomes dos pipelines.
        """
        return list(self._pipelines.keys())

    def remove_pipeline(self, name: str) -> None:
        """
        Remove um pipeline do registro.

        Args:
            name (str): Nome do pipeline a ser removido.
        """
        # TODO: Verificar se existe antes de remover (raise exception se necessário)
        self._pipelines.pop(name, None)

    def run_pipeline(self, pipeline_name: str, input_data: dict):
        logger = logging.getLogger("scene_analysis.pipeline")
        if pipeline_name != "scene_analysis":
            raise ValueError("Pipeline desconhecido: " + pipeline_name)
        logger.info(f"[scene_analysis] Pipeline iniciado | task_id={input_data.get('task_id')} | params={input_data.get('params')}")
        image = load_image(input_data.get("file_path") or input_data.get("media_url"))
        faces = []
        # Plug real do detector
        detector = YOLOFaceDetector(model_path="models/face_detection/yoloface.onnx", config={})
        detected = detector.detect(image)
        for det in detected:
            face = {"box": det["box"], "score": det.get("score")}
            # Landmarks
            if input_data["params"].get("landmark_mode"):
                extractor = FanLandmarkExtractor(model_path="models/face_landmark/fan.onnx", config={})
                face["landmarks"] = extractor.extract(image, [det["box"]])[0]
            # Máscara
            if input_data["params"].get("segment"):
                segmenter = SAM2Segmenter(model_path="models/face_segment/sam2.onnx", config={})
                face["masks"] = segmenter.segment(image, [det["box"]])[0]
            faces.append(face)
        result = {
            "num_faces": len(faces),
            "faces": faces,
            "overlay_url": save_overlay(image, faces),
            "frame_id": input_data["params"].get("frame_id"),
            "timestamp": input_data["params"].get("timestamp"),
            "video_summary": None
        }
        logger.info(f"[scene_analysis] Pipeline concluído | task_id={input_data.get('task_id')} | faces={len(faces)}")
        return result 