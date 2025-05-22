# Módulo `schemas`

## Sumário
- [Visão Geral](#visão-geral)
- [Modelos Pydantic](#modelos-pydantic)
- [Exemplos de Uso](#exemplos-de-uso)
- [Pontos de Extensão](#pontos-de-extensão)
- [Notas e Recomendações](#notas-e-recomendações)
- [Resumo Final](#resumo-final)

---

## Visão Geral
O módulo `schemas` centraliza todos os Pydantic models para requests e responses da API VisioVox Fusion, padronizando contratos, validação, documentação automática e suporte multilíngue (i18n-ready).

---

## Modelos Pydantic
- `MediaProcessRequest`: Parâmetros para processar imagem, vídeo ou áudio.
- `LoginRequest`: Payload de login.
- `RegisterRequest`: Payload de registro.
- `TaskStatusRequest`: Consulta de status de tarefa assíncrona.
- `MediaProcessResponse`: Resposta padronizada com status, output e mensagens.
- `ErrorResponse`: Mensagem de erro multilíngue padrão.
- `UserResponse`: Dados básicos do usuário autenticado.
- `TaskStatusResponse`: Status/resultados de tarefas Celery/Async.
- `MessageResponse`: Mensagens gerais, multilíngues.
- `PaginatedResponse`: Resposta com paginação para listas.
- `TokenResponse`: Resposta JWT/OAuth2.

---

## Exemplos de Uso
```python
from visiovox.apis.schemas import MediaProcessRequest, ErrorResponse, PaginatedResponse
```

---

## Pontos de Extensão
- Adição de novos schemas para features/rotas futuras.
- Campos multilíngues prontos para integração com helper de tradução.
- Suporte a payloads de tasks, webhooks, notificações, etc.

---

## Notas e Recomendações
- Use sempre os schemas para validação e documentação automática.
- Campos message/detail são multilíngues por padrão.
- Expanda conforme surgirem novos fluxos/endpoints.

---

## Resumo Final
O módulo `schemas` padroniza contratos de entrada/saída, erros e mensagens multilíngues, pronto para integração incremental e documentação robusta na API VisioVox Fusion. 