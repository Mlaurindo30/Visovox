"""
Schemas Pydantic para validação de dados na API do VisioVox Fusion.
"""

from typing import Optional, List, Dict, Any, Union
from pydantic import BaseModel, Field
from fastapi import UploadFile

class MediaProcessRequest(BaseModel):
    """Schema para requisição de processamento de mídia."""
    media_type: str = Field(..., description="Tipo da mídia: 'image', 'video', 'audio'.")
    file: Optional[UploadFile] = Field(None, description="Arquivo de mídia enviado via multipart.")
    media_url: Optional[str] = Field(None, description="URL remota para baixar a mídia.")
    params: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Parâmetros opcionais para o pipeline.")

class LoginRequest(BaseModel):
    """
    Payload para login de usuário.
    """
    username: str = Field(..., description="Nome de usuário ou email.")
    password: str = Field(..., description="Senha do usuário.")

class RegisterRequest(BaseModel):
    """
    Payload para registro de novo usuário.
    """
    username: str = Field(..., description="Nome de usuário.")
    password: str = Field(..., description="Senha segura.")
    email: str = Field(..., description="E-mail do usuário.")

class TaskStatusRequest(BaseModel):
    """
    Consulta de status de uma tarefa assíncrona.
    """
    task_id: str = Field(..., description="Identificador único da tarefa Celery/Async.")

# -------------------- RESPOSTAS --------------------

class MediaProcessResponse(BaseModel):
    """Resposta inicial ao enfileirar task de processamento."""
    task_id: str = Field(..., description="ID da tarefa Celery.")
    status: str = Field(..., description="Status inicial: 'queued', 'started'.")
    message: str = Field(..., description="Mensagem multilíngue.")
    detail: Optional[str] = Field(None, description="Detalhe adicional (opcional).")

class ErrorResponse(BaseModel):
    """Resposta padronizada para erros."""
    error: str = Field(..., description="Descrição do erro.")
    message: Optional[str] = Field(None, description="Mensagem adicional do erro.")
    code: Optional[int] = Field(None, description="Código de erro HTTP ou customizado.")

class UserResponse(BaseModel):
    """
    Dados básicos do usuário autenticado.
    """
    user_id: str = Field(..., description="ID único do usuário.")
    username: str = Field(..., description="Nome do usuário.")
    email: str = Field(..., description="E-mail do usuário.")
    roles: Optional[List[str]] = Field(None, description="Lista de roles/perfis do usuário.")

class TaskStatusResponse(BaseModel):
    """Resposta ao consultar status de uma tarefa Celery."""
    task_id: str = Field(..., description="ID da tarefa Celery.")
    status: str = Field(..., description="Status atual da task: 'queued', 'started', 'success', 'failure'.")
    progress: Optional[float] = Field(None, description="Progresso da task (0.0 a 1.0).")
    result: Optional[Dict[str, Any]] = Field(None, description="Resultado final, se disponível.")
    message: Optional[str] = Field(None, description="Mensagem multilíngue.")

class MessageResponse(BaseModel):
    """
    Mensagem informativa multilíngue simples.
    """
    message: Dict[str, str] = Field(..., description="Mensagem por idioma (i18n).")

class PaginatedResponse(BaseModel):
    """
    Resposta genérica para listas paginadas.
    """
    items: List[Any] = Field(..., description="Lista de itens retornados.")
    total: int = Field(..., description="Total de itens disponíveis.")
    page: int = Field(..., description="Número da página atual.")
    size: int = Field(..., description="Tamanho da página (quantos itens por página).")

class TokenResponse(BaseModel):
    """
    Resposta para autenticação JWT/OAuth2.
    """
    access_token: str = Field(..., description="JWT de acesso.")
    token_type: str = Field(..., description="Tipo do token (ex: 'bearer').")
    expires_in: Optional[int] = Field(None, description="Tempo de expiração em segundos.")

class SceneAnalysisRequest(BaseModel):
    """
    Request para análise de cena (imagem ou vídeo).
    Exemplo de uso:
    {
      "media_type": "image",
      "params": {
        "detect_mode": "YOLOFace",
        "landmark_mode": "68",
        "segment": true,
        "max_faces": 3
      }
    }
    """
    media_type: str = Field(..., description='Tipo de mídia ("image" ou "video").')
    file: Optional[UploadFile] = Field(None, description="Arquivo de mídia enviado (upload).")
    media_url: Optional[str] = Field(None, description="URL remota da mídia (opcional).")
    params: Optional[Dict[str, Union[str, int, float, bool]]] = Field(default_factory=dict, description="Parâmetros extras do pipeline. Exemplo: detect_mode, landmark_mode, max_faces.")

class FaceBox(BaseModel):
    """
    Bounding box de uma face detectada.
    """
    x1: float = Field(..., description="Coordenada X do canto superior esquerdo.")
    y1: float = Field(..., description="Coordenada Y do canto superior esquerdo.")
    x2: float = Field(..., description="Coordenada X do canto inferior direito.")
    y2: float = Field(..., description="Coordenada Y do canto inferior direito.")
    width: Optional[float] = Field(None, description="Largura da bounding box (auto).")
    height: Optional[float] = Field(None, description="Altura da bounding box (auto).")
    score: Optional[float] = Field(None, description="Confiança da detecção (0-1).")

class Landmark(BaseModel):
    """
    Landmark facial 2D ou 3D.
    """
    x: float = Field(..., description="Coordenada X.")
    y: float = Field(..., description="Coordenada Y.")
    z: Optional[float] = Field(None, description="Coordenada Z (se disponível, ex: 3D).")
    idx: Optional[int] = Field(None, description="Índice do ponto.")
    name: Optional[str] = Field(None, description="Nome do landmark.")

class FaceMask(BaseModel):
    """
    Máscara segmentada da face (binária ou por atributo).
    """
    mask_type: str = Field(..., description="Tipo de máscara ('sam2', 'xseg', 'parsing', etc).")
    mask_url: Optional[str] = Field(None, description="URL/path da máscara gerada.")
    attributes: Optional[Dict[str, Union[str, float, int]]] = Field(default_factory=dict, description="Atributos presentes na máscara.")

class FaceAttributes(BaseModel):
    """
    Atributos faciais previstos (opcional).
    """
    age: Optional[float] = Field(None, description="Idade estimada.")
    gender: Optional[str] = Field(None, description="Gênero previsto.")
    emotion: Optional[str] = Field(None, description="Emoção predominante.")
    quality: Optional[float] = Field(None, description="Score de qualidade/blur.")
    # Pode expandir para outros atributos.

class FaceDetectionResult(BaseModel):
    """
    Resultado detalhado de uma face detectada.
    """
    box: FaceBox = Field(..., description="Bounding box da face.")
    score: Optional[float] = Field(None, description="Confiança da detecção.")
    landmarks: Optional[List[Landmark]] = Field(None, description="Lista de landmarks (2D/3D).")
    pose: Optional[Dict[str, float]] = Field(None, description="Orientação (pitch, yaw, roll).")
    masks: Optional[List[FaceMask]] = Field(None, description="Máscaras segmentadas.")
    attributes: Optional[FaceAttributes] = Field(None, description="Atributos previstos.")
    embedding: Optional[List[float]] = Field(None, description="Embedding facial para reconhecimento.")

class SceneAnalysisResult(BaseModel):
    """
    Resultado detalhado da análise de cena.
    """
    num_faces: int = Field(..., description="Número de faces detectadas.")
    faces: List[FaceDetectionResult] = Field(..., description="Lista de faces detectadas.")
    masks: Optional[List[FaceMask]] = Field(None, description="Máscaras globais (ex: background, face parsing).")
    overlay_url: Optional[str] = Field(None, description="URL da imagem anotada (bounding boxes, landmarks, etc).")
    frame_id: Optional[int] = Field(None, description="Índice do frame (se vídeo).")
    timestamp: Optional[float] = Field(None, description="Timestamp do frame (se vídeo).")
    video_summary: Optional[Dict[str, Union[int, float, str]]] = Field(None, description="Resumo para vídeos: frames processados, faces por frame, etc.")

class SceneAnalysisResponse(BaseModel):
    """
    Response assíncrona para análise de cena.
    Exemplos de resposta incremental:
    # Detecção básica
    {
      "task_id": "abc123",
      "status": "success",
      "result": {
        "num_faces": 1,
        "faces": [
          { "box": { "x1": 50, "y1": 100, "x2": 200, "y2": 300, "score": 0.99 } }
        ]
      },
      "message": "1 face detected"
    }
    # Com landmarks e máscara
    {
      "task_id": "abc123",
      "status": "success",
      "result": {
        "num_faces": 1,
        "faces": [
          {
            "box": { "x1": 50, "y1": 100, "x2": 200, "y2": 300, "score": 0.99 },
            "landmarks": [ { "x": 72.1, "y": 135.0, "idx": 0, "name": "left_eye" } ],
            "masks": [ { "mask_type": "sam2", "mask_url": "/tmp/mask_abc123.png" } ]
          }
        ],
        "overlay_url": "/tmp/overlay_abc123.png"
      },
      "message": "Face, landmarks and mask returned"
    }
    # Suporte a vídeo
    {
      "task_id": "abc124",
      "status": "success",
      "result": {
        "num_faces": 2,
        "faces": [...],
        "frame_id": 5,
        "timestamp": 0.20,
        "overlay_url": "/tmp/frame5_overlay.png"
      },
      "message": "Frame 5 processed"
    }
    """
    task_id: str = Field(..., description="ID da task Celery para acompanhamento.")
    status: str = Field(..., description='Status ("queued", "started", "success", "failure").')
    result: Optional[SceneAnalysisResult] = Field(None, description="Resultado, se disponível.")
    message: str = Field(..., description="Mensagem multilíngue de status ou erro.")
    detail: Optional[str] = Field(None, description="Detalhes adicionais para debugging ou erro.") 