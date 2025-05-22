# Referência da API

## Padrão de Endpoints
- Todos os domínios seguem o padrão RESTful, com prefixos definidos no `main.py`.
- Exemplos de endpoints:
  - `POST /api/v1/media/process`
  - `POST /api/v1/face/process`
  - `POST /api/v1/voice/process`
  - `POST /api/v1/visual/generate`
  - `POST /api/v1/scene/analyze`
  - `POST /api/v1/sync/process`
  - `POST /api/v1/live/start`
  - `POST /api/v1/models/download`
  - `GET /api/v1/media/status/{task_id}`
  - `GET /api/v1/face/status/{task_id}`
  - ...

## Schemas Genéricos
- Todos os endpoints usam os seguintes schemas:
  - `MediaProcessRequest`
  - `MediaProcessResponse`
  - `TaskStatusResponse`
  - `ErrorResponse`
  - `PaginatedResponse` (para listagens)

### Exemplo de Payload de Requisição
```json
{
  "media_type": "image",
  "media_url": "http://exemplo.com/img.jpg",
  "params": {}
}
```

### Exemplo de Resposta de Sucesso
```json
{
  "status": "pending",
  "task_id": "12345",
  "message": "Processamento enfileirado",
  "detail": "Aguardando execução do pipeline."
}
```

### Exemplo de Resposta de Erro
```json
{
  "error": "Tipo de mídia inválido",
  "detail": "O campo media_type deve ser 'image', 'video' ou 'audio'."
}
```

## Status dos Endpoints
- Todos os endpoints principais estão disponíveis e testados.
- Testes automatizados garantem que os contratos de entrada/saída estão corretos. 