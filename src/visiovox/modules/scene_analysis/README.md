# Módulo `scene_analysis` — VisioVox Fusion

## Visão Geral
- Análise de cena (imagem/vídeo): detecção facial, landmarks, segmentação, atributos, overlays.
- Schemas incrementais, plug & play de submódulos.
- Pronto para upload, polling, overlays, feedback incremental.

## Exemplos de Uso
- Request/response reais no README.
- Upload via Swagger, cURL, frontend React.
- Polling incremental de status.

## FAQ & HowTo
- Como expandir schemas, plugar módulos, testar, debugar, integrar frontend.
- Veja `FAQ.md` para detalhes.

## Dicas de Expansão
- Plugue detectores/segmentadores reais conforme disponibilidade.
- Use campos opcionais para evolução incremental.
- Nunca remova campos antigos.

## Integração com Frontend
- Exemplo React em `frontend_example/`.
- Pronto para Vue/Svelte.

## Observabilidade
- Logging estruturado, healthcheck detalhado, pronto para Sentry/Prometheus.

## Troubleshooting
- Logs detalhados, healthcheck, FAQ.

---

## Exemplo de Request — SceneAnalysisRequest

### Detecção Facial em Imagem (com parâmetros customizados)
```json
{
  "media_type": "image",
  "params": {
    "detect_mode": "YOLOFace",
    "landmark_mode": "68",
    "segment": true,
    "max_faces": 3
  }
}
```
> Para upload de arquivo, use multipart/form-data no Swagger ou client HTTP.

---

## Exemplo de Response — SceneAnalysisResponse

### Resposta Básica (apenas detecção facial)
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "num_faces": 1,
    "faces": [
      {
        "box": { "x1": 50, "y1": 100, "x2": 200, "y2": 300, "score": 0.99 }
      }
    ]
  },
  "message": "1 face detected"
}
```

### Resposta com Landmarks e Máscara
```json
{
  "task_id": "abc123",
  "status": "success",
  "result": {
    "num_faces": 1,
    "faces": [
      {
        "box": { "x1": 50, "y1": 100, "x2": 200, "y2": 300, "score": 0.99 },
        "landmarks": [
          { "x": 72.1, "y": 135.0, "idx": 0, "name": "left_eye" },
          { "x": 120.5, "y": 140.2, "idx": 1, "name": "right_eye" }
        ],
        "masks": [
          { "mask_type": "sam2", "mask_url": "/tmp/mask_abc123.png" }
        ]
      }
    ],
    "overlay_url": "/tmp/overlay_abc123.png"
  },
  "message": "Face, landmarks and mask returned"
}
```

### Resposta para Vídeo (frame a frame)
```json
{
  "task_id": "abc124",
  "status": "success",
  "result": {
    "num_faces": 2,
    "faces": [
      { "box": { "x1": 30, "y1": 80, "x2": 180, "y2": 260, "score": 0.95 } },
      { "box": { "x1": 220, "y1": 90, "x2": 340, "y2": 250, "score": 0.92 } }
    ],
    "frame_id": 5,
    "timestamp": 0.20,
    "overlay_url": "/tmp/frame5_overlay.png"
  },
  "message": "Frame 5 processed"
}
```

---

## Campos e Uso Incremental
- **faces[].box**: sempre presente (detecção facial básica).
- **faces[].landmarks, faces[].masks, faces[].attributes, faces[].embedding**: só aparecem quando o submódulo correspondente está plugado.
- **params**: aceita qualquer parâmetro customizado do pipeline (ex: detect_mode, landmark_mode, segment, max_faces).
- **frame_id, timestamp**: usados para vídeo, identificando cada frame processado.
- **overlay_url, mask_url**: caminhos temporários para artefatos gerados (imagens, máscaras).

## Dicas de Integração
- Comece só com detecção facial (box/score). Plugue novos campos conforme evoluir o pipeline.
- Para vídeo, retorne um SceneAnalysisResult por frame.
- Nunca remova campos antigos: só adicione novos, mantendo retrocompatibilidade.

## Integração com API
- Os schemas estão prontos para uso direto nos endpoints REST e tasks Celery.
- O campo `params` permite pipelines altamente configuráveis.
- O módulo está pronto para integração incremental com o Orchestrator e PipelineManager.

---

## Referências
- [YOLOFace](https://github.com/deepinsight/insightface/tree/master/detection/scrfd)
- [SAM2](https://segment-anything.com/)
- [Pydantic](https://docs.pydantic.dev/)

---

**Módulo pronto para evolução incremental, onboarding e integração full stack!** 